# ptx_parser.py
# -------------------------------------------------------------------------------------
# Professional-level parser for NVIDIA PTX IR.
# This module extracts function/kernel boundaries, instructions, registers, etc.
# -------------------------------------------------------------------------------------

import re
from typing import Dict, Any

class PtxParser:
    """
    PtxParser is responsible for reading raw PTX text and converting it into a structured
    representation. This includes identifying kernels, instructions, and resources used
    (registers, shared memory, etc.).
    """

    def __init__(self):
        self.kernels = {}

    def parse_ptx(self, ptx_text: str) -> Dict[str, Any]:
        """
        Parses the raw PTX text and populates self.kernels with structured data.
        Returns:
            dict: A dictionary of kernels, each with instructions and resources info.
        """
        # Regex to match kernel definitions (e.g., .visible .entry myKernel)
        kernel_pattern = re.compile(r"\.visible\s+\.entry\s+([\w_]+)\s*\(.*?\)\s*\{")
        instruction_pattern = re.compile(r"^\s*([a-zA-Z0-9_.]+)\s+([^\s;]+);", re.MULTILINE)

        current_kernel = None

        # Split the PTX text by lines and iterate
        for line in ptx_text.splitlines():
            kernel_match = kernel_pattern.match(line)
            if kernel_match:
                # Start of a new kernel
                current_kernel = kernel_match.group(1)
                self.kernels[current_kernel] = {"instructions": []}
                continue

            if current_kernel:
                # Match instructions inside the current kernel
                instruction_match = instruction_pattern.match(line)
                if instruction_match:
                    instruction = {
                        "opcode": instruction_match.group(1),
                        "operands": instruction_match.group(2),
                    }
                    self.kernels[current_kernel]["instructions"].append(instruction)

        return self.kernels
