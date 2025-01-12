# visualizer.py
# -------------------------------------------------------------------------------------
# Contains functions that convert the IR comparison into human-friendly or graphical formats.
# -------------------------------------------------------------------------------------

import networkx as nx
from typing import Dict, Any

class Visualizer:
    """
    Visualizer constructs a graph from the PTX instructions (optionally) and helps present
    the changes in a structured, user-friendly manner.
    """

    def create_instruction_graph(self, ptx_data: Dict[str, Any], kernel_name: str):
        """
        Creates a directed graph of instructions for a particular kernel. This can highlight
        potential data or control dependencies (basic approach for demonstration).
        """
        # For demonstration, we'll just create a naive chain of instructions:
        G = nx.DiGraph()
        instructions = ptx_data[kernel_name]["instructions"]

        # Add nodes
        for idx, ins in enumerate(instructions):
            node_label = f"{idx}: {ins['opcode']} {ins['operands']}"
            G.add_node(idx, label=node_label)

        # Create edges as a simple chain
        for i in range(len(instructions) - 1):
            G.add_edge(i, i + 1)

        return G

    def render_graph(self, graph, output_file: str = "kernel_graph.png"):
        """
        Renders the given networkx graph as an image file (e.g., PNG).
        """
        import pygraphviz
        from networkx.drawing.nx_agraph import to_agraph

        A = to_agraph(graph)
        A.layout("dot")
        A.draw(output_file)

    def text_report(self, diff_report: Dict[str, Any]) -> str:
        """
        Generates a textual summary from the diff report. 
        """
        lines = []
        if diff_report["new_kernels"]:
            lines.append("New Kernels Found: " + ", ".join(diff_report["new_kernels"]))
        if diff_report["removed_kernels"]:
            lines.append("Removed Kernels: " + ", ".join(diff_report["removed_kernels"]))

        for kernel, changes in diff_report["changed_kernels"].items():
            lines.append(f"Changes in {kernel}:")
            lines.append(changes["instruction_diff"])
            lines.append("")

        return "\n".join(lines)

