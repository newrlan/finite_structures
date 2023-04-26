from rubik import Permutation
import pytest


def test_permutation_mul():

    p = Permutation()
    q = p * [1, 3, 2, 4]

    assert q.apply(1) == 3
    assert q.apply(2) == 4
    assert q.apply(3) == 2
    assert q.apply(4) == 1
    assert len(q._perm) == 4


def test_permutation_cycle():

    p = Permutation()
    q = p * [1, 3, 2, 4] * [5, 6]

    cycle = q.cycles()
    assert len(cycle) == 2
    assert cycle[0] == [1,3,2,4]
    assert cycle[1] == [5, 6]
