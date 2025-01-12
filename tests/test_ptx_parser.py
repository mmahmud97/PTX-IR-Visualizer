import pytest
from ptx_parser import PtxParser


def test_parse_single_kernel():
    """
    Test parsing a single kernel with one instruction.
    """
    parser = PtxParser()
    sample_ptx = """
    .visible .entry myKernel() {
        mov.b32 %r1, %r2;
    }
    """
    result = parser.parse_ptx(sample_ptx)
    assert "myKernel" in result
    assert len(result["myKernel"]["instructions"]) == 1
    assert result["myKernel"]["instructions"][0]["opcode"] == "mov"
    assert result["myKernel"]["instructions"][0]["modifier"] == "b32"
    assert result["myKernel"]["instructions"][0]["operands"] == "%r1, %r2"

def test_parse_multiple_kernels():
    """
    Test parsing multiple kernels.
    """
    parser = PtxParser()
    sample_ptx = """
    .visible .entry kernelA() {
        mov.b32 %r1, %r2;
        add.f32 %f1, %f2, %f3;
    }
    .visible .entry kernelB() {
        sub.s32 %r4, %r5, %r6;
    }
    """
    result = parser.parse_ptx(sample_ptx)
    assert "kernelA" in result
    assert "kernelB" in result
    assert len(result["kernelA"]["instructions"]) == 2
    assert len(result["kernelB"]["instructions"]) == 1

def test_empty_ptx():
    """
    Test parsing an empty PTX string.
    """
    parser = PtxParser()
    sample_ptx = ""
    result = parser.parse_ptx(sample_ptx)
    assert result == {}

def test_malformed_ptx():
    """
    Test parsing a malformed PTX string.
    """
    parser = PtxParser()
    sample_ptx = """
    .visible .entry kernelA() {
        mov.b32 %r1, %r2;
        add.f32 %f1 %f2 %f3;  # Missing commas
    }
    """
    result = parser.parse_ptx(sample_ptx)
    assert "kernelA" in result
    assert len(result["kernelA"]["instructions"]) == 2
