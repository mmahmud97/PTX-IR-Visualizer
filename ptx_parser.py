# ptx_parser.py
# -------------------------------------------------------------------------------------
# Professional-level parser for NVIDIA PTX IR.
# This module extracts function/kernel boundaries, instructions, registers, etc.
# -------------------------------------------------------------------------------------

import re
from typing import Dict, Any, List

class PtxParser:
    """
    PtxParser is responsible for reading raw PTX text and converting it into a structured
    representation. This includes identifying kernels, instructions, and resources used
    (registers, shared memory, etc.).
    """

    def __init__(self):
        # We store kernels in a dictionary keyed by the kernel name, each containing
        # detailed information about instructions and resource usage.
        self.kernels = {}

    def parse_ptx(self, ptx_text: str) -> Dict[str, Any]:
        """
        Parses the raw PTX text and populates self.kernels with structured data.
        Returns:
            dict: A dictionary of kernels, each with instructions and resources info.
        """

        # Regex to match kernel definitions (e.g. .visible .entry _Z6kernel...)
        kernel_pattern = re.compile(r"\.visible\s+\.entry\s+([\w_]+)\((.*?)\)")

        # Regex to match PTX instructions - approximate structure
        instruction_pattern = re.compile(r"^\s*([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)\s+(.*);", re.MULTILINE)

        # Find all kernel definitions
        for match in kernel_pattern.finditer(ptx_text):
            kernel_name = match.group(1)
            # Initialize an empty structure for each kernel
            self.kernels[kernel_name] = {
                "params": match.group(2),
                "instructions": []
            }

        # Find all instructions
        instructions = instruction_pattern.findall(ptx_text)
        # instructions is a list of tuples: (opcode, modifier, operands)

        # For simplicity, we assume instructions belong to the last found kernel
        current_kernel_name = None
        lines = ptx_text.split("\n")
        for line in lines:
            # Check if a new kernel is starting
            kernel_match = kernel_pattern.search(line)
            if kernel_match:
                current_kernel_name = kernel_match.group(1)

            # If line matches an instruction, store it in current kernel
            ins_match = instruction_pattern.search(line)
            if ins_match and current_kernel_name is not None:
                opcode = ins_match.group(1)
                modifier = ins_match.group(2)
                operands = ins_match.group(3)
                self.kernels[current_kernel_name]["instructions"].append({
                    "opcode": opcode,
                    "modifier": modifier,
                    "operands": operands.strip()
                })

        return self.kernels

