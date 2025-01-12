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

    def parse_ptx(self, ptx_text: str) -> Dict[str, Any]:
        """
        Parses the raw PTX text and populates the kernel structure with instructions.
        Returns:
            dict: A dictionary of kernels, each with instructions and resources info.
        """
        # Dictionary to store parsed kernels
        kernels = {}

        # Regex to match kernel definitions
        kernel_pattern = re.compile(r"\.visible\s+\.entry\s+([\w_]+)\s*\((.*?)\)")
        instruction_pattern = re.compile(r"^\s*([a-zA-Z0-9_.]+)\s+(.*?);", re.MULTILINE)

        # Find all kernel definitions
        for match in kernel_pattern.finditer(ptx_text):
            kernel_name = match.group(1)
            kernels[kernel_name] = {"instructions": []}

            # Extract instructions
            instructions = instruction_pattern.findall(ptx_text)
            for ins in instructions:
                opcode, operands = ins
                kernels[kernel_name]["instructions"].append({
                    "opcode": opcode,
                    "operands": operands.strip()
                })

        return kernels
