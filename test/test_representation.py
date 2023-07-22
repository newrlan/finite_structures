from pathlib import Path
import pytest
import os
from rubik.permutation import Permutation
from rubik.representations import InvoluteRepresentation


# def test_InvoluteRepresentation__square_read():
#     square = ["WRR", "WWR", "BRG"]
#     square = [list(x) for x in square]
#     res = InvoluteRepresentation()._square_prepare(square)
#     assert res['W1'] == 'W'
#     assert res['W7'] == 'B'
#     assert res['W4'] == 'W'
#     assert res['W5'] == 'W'
#     assert res['W9'] == 'G'


@pytest.fixture()
def db_states(tmp_path):

    action_state = {
        '': [
                "BYO",
                "OYW",
                "GOR",
                "YGG",
                "GOR",
                "RBO",
                "WBW",
                "BWB",
                "WRY",
                "YBY",
                "OWW",
                "OYY",
                "RBO",
                "BYG",
                "RGG",
                "BOY",
                "OBG",
                "RWW",
                "RGR",
            ],

        'b': [
                "BYO",
                "OYW",
                "GOR",
                "RGR",
                "WRG",
                "BBO",
                "WOR",
                "OWW",
                "WRY",
                "YBY",
                "GGY",
                "OYY",
                "RBO",
                "BYG",
                "RGG",
                "BOY",
                "OBG",
                "RWW",
                "BWB",
            ],

        'bo': [
                "BYO",
                "RGO",
                "GOY",
                "RRW",
                "YYO",
                "BBO",
                "WOR",
                "OWW",
                "WRY",
                "YBY",
                "GGG",
                "OYG",
                "RBY",
                "BYG",
                "RGW",
                "BOB",
                "OBW",
                "RWR",
                "BWG",
            ],

        'bow': [
                    "BYO",
                    "BGO",
                    "OOY",
                    "BRW",
                    "RYO",
                    "GBO",
                    "ROR",
                    "YWW",
                    "BRY",
                    "WBY",
                    "GGG",
                    "OYG",
                    "RBY",
                    "BYG",
                    "RGW",
                    "OWY",
                    "BRO",
                    "WWB",
                    "GRW",
                ],
    }

    for key in action_state:
        file_name = tmp_path / f'state_{key}.txt'
        with open(file_name, 'w') as f:
            f.write('\n'.join(action_state[key]))

    return tmp_path



@pytest.mark.parametrize('word', ['b', 'bo', 'bow'])
def test_InvoluteRepresentation_permutation(word, db_states):

    st0 = InvoluteRepresentation.load(db_states / 'state_.txt')
    p = st0.permutation()

    ans = Permutation()
    for c in word:
        ans = ans * st0._actions.get(c.upper())

    st1 = InvoluteRepresentation.load(db_states / f'state_{word}.txt')
    q = st1.permutation()
    print(p**-1 * q)
    print(ans)

    assert p**-1 * q == ans


@pytest.mark.parametrize('word', ['b', 'bo', 'bow'])
def test_InvoluteRepresentation_apply(word, db_states):

    st0 = InvoluteRepresentation.load(db_states / 'state_.txt')
    st0.apply(word)
    p = st0.permutation()

    st1 = InvoluteRepresentation.load(db_states / f'state_{word}.txt')
    q = st1.permutation()
    assert p == q

    




# @pytest.mark.parametrize('action', ['B', 'BW'])
# def test_InvoluteRepresentation_action(action):
# 
#     path = Path(os.path.dirname(__file__))
# 
#     file_name = f'state_action_{action}.txt'
#     state1 = InvoluteRepresentation.load(path / file_name)
#     state0 = InvoluteRepresentation.load(path / 'state_init.txt')
# 
#     state0.apply(action)
#     assert state0.state == state1.state
