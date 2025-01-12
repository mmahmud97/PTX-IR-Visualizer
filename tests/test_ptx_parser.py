import pytest
from ptx_parser import PtxParser

def test_parse_ptx():
    parser = PtxParser()
    sample_ptx = """
    .visible .entry myKernel() {
        mov.b32 %r1, %r2;
    }
    """
    result = parser.parse_ptx(sample_ptx)
    assert "myKernel" in result
    assert len(result["myKernel"]["instructions"]) == 1

