from math import comb
from rubik.words import total_words_volume, word, ACT, _combination_of_splits, CycleLexica
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
    

@pytest.mark.parametrize('n, k, answer', [
    (7, 0, 0),
    (7, 1, 6),
    (7, 2, 1890),
    (7, 3, 36120),
    (7, 4, 126000),
    (7, 5, 100800),
])
def test__combination_of_splits(n, k, answer):
    hyp = _combination_of_splits(n, k)
    assert answer == hyp * comb(6, k)


def test_CycleLexica_add():

    cl = CycleLexica(3)
    cl.add('OOBOYOOBBBOOBOYOOBBB')


def test_CycleLexica_save_load(tmp_path):
    words_list = [
        'OOBOYOOBBBOOBOYOOBBB',
        'OOBBBOOBOYOOBBBOOBOY',
        'OOBOYOOYYYOOBOYOOYYY',
        'OOYYYOOBOYOOYYYOOBOY',
        'OOBOYOGRWOOOBOYOGRWO',
        'OGRWOOOBOYOGRWOOOBOY',
        'OOBYWBGORGOOBYWBGORG',
        'BGORGOOBYWBGORGOOBYW',
        'OOBYWBGROGOOBYWBGROG',
        'BGROGOOBYWBGROGOOBYW',
        'OOBYWGBORGOOBYWGBORG',
    ]
    # Arrange
    cl = CycleLexica(3)
    for w in words_list:
        cl.add(w)

    # Act
    f_name = tmp_path / 'lexica.txt'
    cl.save(f_name)
    new_cl = CycleLexica.load(f_name)

    # Assert
    assert new_cl.dim == 3
    assert len(new_cl.vocab) == 8
