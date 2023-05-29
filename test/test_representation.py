import pytest
from rubik.representations import InvoluteRepresentation


def test_InvoluteRepresentation__square_read():
    square = ["WRR", "WWR", "BRG"]
    square = [list(x) for x in square]
    res = InvoluteRepresentation()._square_prepare(square)
    assert res['W1'] == 'W'
    assert res['W7'] == 'B'
    assert res['W4'] == 'W'
    assert res['W5'] == 'W'
    assert res['W9'] == 'G'


@pytest.fixture()
def state(tmp_path):

    lines = [
        "BYO",
        "WOG",
        "WOY",
        "BOB",
        "WBY",
        "BBB",
        "BBB",
        "RRR",
        "RRY",
        "GRR",
        "YYO",
        "RYO",
        "YYO",
        "GGY",
        "GGG",
        "WGO",
        "RWG",
        "WWO",
        "WWO",
    ]

    file_name = tmp_path / 'state'
    with open(file_name, 'w') as f:
        f.write('\n'.join(lines))

    return file_name


def test_InvoluteRepresentation__vertex_permutation():
    state = {'B3': 'O9', 'O9': 'Y3', 'Y3': 'B3',
             'G9': 'B9', 'W3': 'R3', 'O1': 'Y1',
             'B9': 'G9', 'R3': 'W3', 'Y1': 'O1',
            }

    perm = InvoluteRepresentation._vertex_state_permutation(state)
    assert perm.len() == 2
    assert perm.apply(2) == 4


def test_InvoluteRepresentation__edges_permutation():
    state = {'G4': 'R8', 'R8': 'G4',
             'R4': 'R6', 'W4': 'Y4',
             'R6': 'R4', 'Y4': 'W4',
            }

    perm = InvoluteRepresentation._edges_state_permutation(state)
    print(perm)
    assert perm.len() == 2
