# transform_analyzer.py
# -------------------------------------------------------------------------------------
# Analyzes differences between two or more PTX IR representations.
# Provides functionalities to highlight optimizations or regressions.
# -------------------------------------------------------------------------------------

from typing import Dict, Any
import difflib

class TransformAnalyzer:
    """
    TransformAnalyzer compares the structured representation of PTX code from multiple
    stages or versions. It identifies changes in instruction count, kernel presence,
    resource usage, etc.
    """

    def compare_kernels(self, ptx_a: Dict[str, Any], ptx_b: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compares kernel data from two PTX sets.
        Returns:
            dict: A report highlighting changes in instruction count, new/removed kernels, etc.
        """
        report = {
            "new_kernels": [],
            "removed_kernels": [],
            "changed_kernels": {}
        }

        kernels_a = set(ptx_a.keys())
        kernels_b = set(ptx_b.keys())

        # Identify new or removed kernels
        report["new_kernels"] = list(kernels_b - kernels_a)
        report["removed_kernels"] = list(kernels_a - kernels_b)

        # Identify changed kernels
        common_kernels = kernels_a.intersection(kernels_b)
        for kernel_name in common_kernels:
            instructions_a = ptx_a[kernel_name]["instructions"]
            instructions_b = ptx_b[kernel_name]["instructions"]

            if instructions_a != instructions_b:
                diff = self.generate_instruction_diff(instructions_a, instructions_b)
                if diff:
                    report["changed_kernels"][kernel_name] = {
                        "instruction_diff": diff
                    }

        return report


    def generate_instruction_diff(self, instructions_a, instructions_b):
        """
        Generates a textual diff of instructions between two lists.
        """
        # Convert instruction dicts to strings for easier diff
        lines_a = [f"{ins['opcode']} {ins['modifier']} {ins['operands']}" for ins in instructions_a]
        lines_b = [f"{ins['opcode']} {ins['modifier']} {ins['operands']}" for ins in instructions_b]

        diff = difflib.unified_diff(lines_a, lines_b, lineterm="", fromfile="PTX_A", tofile="PTX_B")
        return "\n".join(diff)
