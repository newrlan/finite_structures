import pytest
from rubik.representations import InvoluteRepresentation


def test_InvoluteRepresentation__square_read():
    square = ["WRR", "WWR", "BRG"]
    square = [list(x) for x in square]
    res = InvoluteRepresentation()._square_prepare(square)
    assert res['W1'] == 'W'
    assert res['W7'] == 'R'
    assert res['W4'] == 'W'
    assert res['W5'] == 'R'
    assert res['W8'] == 'G'
