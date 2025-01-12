# run_visualizer.py
# -------------------------------------------------------------------------------------
# Command-line interface to generate PTX IR transformations and produce a textual or graphical report.
# -------------------------------------------------------------------------------------

import argparse
from ptx_parser import PtxParser
from transform_analyzer import TransformAnalyzer
from visualizer import Visualizer

def main():
    parser = argparse.ArgumentParser(description="PTX IR Transformation Visualizer CLI")
    parser.add_argument("--ptx_files", nargs="+", help="List of PTX files to compare", required=True)
    args = parser.parse_args()

    if len(args.ptx_files) < 2:
        print("Please provide at least two PTX files to compare.")
        return

    # Parse the first and second PTX for comparison
    with open(args.ptx_files[0], 'r') as f:
        ptx_text_a = f.read()

    with open(args.ptx_files[1], 'r') as f:
        ptx_text_b = f.read()

    parser_a = PtxParser()
    parser_b = PtxParser()

    data_a = parser_a.parse_ptx(ptx_text_a)
    data_b = parser_b.parse_ptx(ptx_text_b)

    analyzer = TransformAnalyzer()
    diff_report = analyzer.compare_kernels(data_a, data_b)

    # Print the diff report
    if diff_report["changed_kernels"]:
        for kernel, changes in diff_report["changed_kernels"].items():
            print(f"\nChanges in {kernel}:")
            print(changes["instruction_diff"])
    else:
        print("\nNo differences found.")

    # Optionally, render a graph for a kernel that appears in both
    common_kernels = set(data_a.keys()).intersection(set(data_b.keys()))
    if common_kernels:
        visual = Visualizer()
        kernel = list(common_kernels)[0]
        graph_a = visual.create_instruction_graph(data_a, kernel)
        visual.render_graph(graph_a, output_file=f"{kernel}_graph_A.png")
        graph_b = visual.create_instruction_graph(data_b, kernel)
        visual.render_graph(graph_b, output_file=f"{kernel}_graph_B.png")
        print(f"Graphs rendered for kernel: {kernel}")

if __name__ == "__main__":
    main()
