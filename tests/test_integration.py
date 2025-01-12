import pytest
import subprocess
import os

def test_cli_comparison(tmp_path):
    # Suppose we have run_visualizer.py as a CLI
    ptx_file1 = tmp_path / "test1.ptx"
    ptx_file2 = tmp_path / "test2.ptx"
    ptx_file1.write_text(".visible .entry kernelTest() { mov.b32 %r1, %r2; }")
    ptx_file2.write_text(".visible .entry kernelTest() { mov.b32 %r1, %r3; }")

    result = subprocess.run([
        "python", "run_visualizer.py",
        "--ptx_files", str(ptx_file1), str(ptx_file2)
    ], capture_output=True, text=True)

    assert "Graphs rendered" in result.stdout
    # We confirm that the text diff is shown
    assert "kernelTest" in result.stdout

