import pytest
from rubik.permutation import Permutation
from rubik.solver import Puzzle, permutation_triplets, separate_swaps, swaps_to_triplets
from random import choice, randint

from rubik.words import ACT, word


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
    p = q ** 2  # гарантируем генерацию перестановки четной в каждой подгруппе

    res = Permutation()
    for tr in swaps_to_triplets(p.swaps()):
        res = res.apply_cycle(tr)

    assert p == res


@pytest.mark.parametrize('n_times', range(5))
def test_permutation_triplets(n_times, permutation):
    _, q = permutation
    p = q ** 2  # гарантируем генерацию перестановки четной в каждой подгруппе

    res = Permutation()
    for tr in permutation_triplets(p):
        res = res.apply_cycle(tr)

    assert p == res


@pytest.mark.parametrize('n_times', range(100))
def test_even(n_times, permutation):
    w, p = permutation
    assert len(p.swaps()) % 2 == 0, f'Word {w} permutation {p}'


@pytest.mark.parametrize('n_times', range(100))
def test_Puzzle_word(n_times, permutation):
    ws, p = permutation
    rubik = Puzzle()
    rubik.apply(ws)
    new_ws = rubik.word()
    q = word(new_ws)
    assert p == q
    # assert ws == rubik.word()
