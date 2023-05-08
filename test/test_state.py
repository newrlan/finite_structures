import pytest
from pathlib import Path
import os
from rubik.permutation import Permutation

from rubik.state import Rubik
from rubik.coloring import Vector, Color


def test_Rubik_init():
    cube = Rubik()
    p = cube.permutation()
    assert p.len() == 0
    assert p.deg() == 1


def test_Rubik_read():
    abs_path = os.path.dirname(__file__)
    file = os.path.join(abs_path, 'state_300423.txt')
    file = Path(file)
    state = Rubik.load(file)
    assert state.coloring[Vector(1, 1, 1)] == Vector(-1, 1, 1)


def test_Rubik_permutation():
    p = Permutation().apply_cycle([1, 2, 8]).apply_cycle([9, 10, 11, 14])
    cell = Rubik().cells
    coloring = dict()
    for k, v in p._perm.items():
        coloring[cell[v - 1]] = cell[k - 1]

    cube = Rubik(coloring)
    q = cube.permutation()
    assert q == p


@pytest.mark.parametrize('color', Color)
def test_Rubik_act(color):
    cube = Rubik()
    cube.act(color)
    p = cube.permutation()
    assert p.len() == 8
    assert p.deg() == 4


# def test_Rubik_apply_word():
#     abs_path = os.path.dirname(__file__)
#     file = os.path.join(abs_path, 'state_300423.txt')
#     file = Path(file)
#     cube = Rubik.load(file)
# 
#     p = cube.permutation(subgroup='vertex')
#     word = RubikSmallGroup().permutation2word(p)
# 
#     cube.apply(word)
#     q = cube.permutation(subgroup='vertex')
#     assert q.len() == 0
