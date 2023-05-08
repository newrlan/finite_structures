from rubik.words import total_words_volume, word, ACT
from rubik.state import Rubik
import pytest


check_word_list = [
    "gbr",
    'oywgbrowygbr',
]


@pytest.mark.parametrize('ws', check_word_list)
def test_word(ws):
    pw = word(ws)
    cube = Rubik()
    cube.apply(ws.upper())
    pc = cube.permutation()
    assert pw == pc


@pytest.mark.parametrize('act', 'OBYGWR')
def test_ACT(act):
    cube = Rubik()
    cube.apply(act)
    pc = cube.permutation()
    pa = ACT[act]
    assert pa == pc


@pytest.mark.parametrize('n, k, answer', [(4, 0, 6**4),
                                          (5, 0, 6**5),
                                          (5, 2, 7770),
                                          (7, 4, 241920),
                                          (7, 2, 279930),
                                          (7, 3, 278040),
                                          (6, 1, 46656),
                                          (6, 8, 0),
                                          ])
def test_total_words_volume(n, k, answer):
    total = total_words_volume(n, k)
    assert total == answer
    
