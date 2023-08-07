from pathlib import Path
import pytest
import os
from rubik.permutation import Permutation
from rubik.representations import InvoluteRepresentation


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
        'bowr': [
                    "BYO",

                    "BGO",
                    "OOY",
                    "BRW",

                    "RYO",
                    "GBO",
                    "BWG",

                    "WBY",
                    "BRW",
                    "YYW",

                    "RGG",
                    "OYG",
                    "RBY",

                    "GYG",
                    "OGW",
                    "RWY",

                    "BRO",
                    "RWB",
                    "ORW",
                ],
        'bowrg': [
                    "BYO",

                    "YBR",
                    "OOY",
                    "BRW",

                    "RYO",
                    "GBO",
                    "BWG",

                    "WBY",
                    "BRW",
                    "ORB",

                    "RGG",
                    "OYG",
                    "YYW",

                    "ROG",
                    "WGY",
                    "YWG",

                    "BGO",
                    "RWB",
                    "ORW",
                ],
        'bowrgy': [
                    "BYO",

                    "YBO",
                    "OOO",
                    "BRG",

                    "RYY",
                    "GBW",
                    "BWB",

                    "WBR",
                    "BRO",
                    "ORG",

                    "YOR",
                    "YYG",
                    "WGG",

                    "RYW",
                    "WGY",
                    "YWG",

                    "BGO",
                    "RWB",
                    "ORW",
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

    assert p**-1 * q == ans


@pytest.mark.parametrize('word', ['b', 'bo', 'bow'])
def test_InvoluteRepresentation_apply(word, db_states):

    st0 = InvoluteRepresentation.load(db_states / 'state_.txt')
    st0.apply(word)
    p = st0.permutation()

    st1 = InvoluteRepresentation.load(db_states / f'state_{word}.txt')
    q = st1.permutation()
    assert p == q


@pytest.mark.parametrize('left, right', [
            ('', 'b'),
            ('b', 'bo'),
            ('bo', 'bow'),
            ('bow', 'bowr'),
            ('bowr', 'bowrg'),
            ('bowrg', 'bowrgy'),
         ]
    )
def test_InvoluteRepresentation_actions(left, right, db_states):

    # arrange
    l = InvoluteRepresentation.load(db_states / f'state_{left}.txt')
    r = InvoluteRepresentation.load(db_states / f'state_{right}.txt')

    # act
    act = right[-1].upper()
    l.apply(act)

    # assert
    assert l.permutation() == r.permutation()


@pytest.mark.parametrize('act, ans', [
            ('o', Permutation().apply_cycle(['OY', 'BO', 'OW', 'GO'],
                                            ['BOW', 'GOW', 'GOY', 'BOY'])
             ),
            ('b', Permutation().apply_cycle(['BY', 'BR', 'BW', 'BO'],
                                            ['BOW', 'BOY', 'BRY', 'BRW'])
             ),
         ]
    )
def test_InvoluteRepresentation_permutation_full_false(act, ans):
    cl = InvoluteRepresentation()
    cl.apply(act)
    p = cl.permutation(False)
    assert p == ans
