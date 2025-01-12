import pytest
from transform_analyzer import TransformAnalyzer

def test_compare_kernels():
    analyzer = TransformAnalyzer()
    ptx_a = {
        "kernelA": {"instructions": [{"opcode":"mov","modifier":"b32","operands":"%r1, %r2"}]}
    }
    ptx_b = {
        "kernelA": {"instructions": [{"opcode":"mov","modifier":"b32","operands":"%r1, %r3"}]},
        "kernelB": {"instructions": []}
    }
    report = analyzer.compare_kernels(ptx_a, ptx_b)
    assert "kernelB" in report["new_kernels"]
    assert "kernelA" in report["changed_kernels"]

