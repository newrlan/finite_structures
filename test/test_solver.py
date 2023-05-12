import pytest
from rubik.permutation import Permutation
from rubik.solver import separate_swaps, swaps_to_triplets
from random import choice, randint

from rubik.words import ACT


@pytest.fixture
def permutation():
    p = Permutation()
    w = ''
    for _ in range(randint(2, 20)):
        color = choice('OBYGWR')
        p *= ACT[color]
        w += color
    return w, p


@pytest.mark.parametrize('n_times', range(5))
def test_separator(n_times, permutation):
    _, perm = permutation
    vertex, edge = separate_swaps(perm)
    v = Permutation()
    for sw in vertex:
        v = v.apply_cycle(sw)
    e = Permutation()
    for sw in edge:
        e = e.apply_cycle(sw)

    assert perm == v * e


@pytest.mark.parametrize('n_times', range(5))
def test_swaps_to_triplets(n_times, permutation):
    _, q = permutation
    p = q ** 2  # гарантируем доставание перестановки четной в каждой подгруппе

    res = Permutation()
    for tr in swaps_to_triplets(p.swaps()):
        res = res.apply_cycle(tr)

    assert p == res
