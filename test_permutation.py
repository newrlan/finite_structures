from permutation import Permutation, RubikSmallGroup
import pytest


def test_permutation_mul():

    p = Permutation()
    q = Permutation({1: 3, 3: 2, 2: 4, 4: 1})
    pq = p * q

    assert pq.apply(1) == 3
    assert pq.apply(2) == 4
    assert pq.apply(3) == 2
    assert pq.apply(4) == 1
    assert len(pq._perm) == 4

    p = Permutation({1: 2, 2: 3, 3: 4, 4: 1})
    pq = p * q
    assert pq.apply(1) == 4
    assert pq.apply(2) == 2
    assert pq.apply(3) == 1
    assert pq.apply(4) == 3
    assert len(pq._perm) == 3


def test_permutation_cycle():

    p = Permutation()
    q = p.apply_cycle([1, 3, 2, 4]).apply_cycle([5, 6])

    cycle = q.cycles()
    assert len(cycle) == 2
    assert cycle[0] == [1, 3, 2, 4]
    assert cycle[1] == [5, 6]


swaps = [
    ((1, 3), (2, 4)),
    ((2, 3), (2, 4)),
    ((1, 2), (2, 4)),
    ((1, 2), (4, 2)),
    ((1, 4), (1, 4)),
]


@pytest.mark.parametrize('swap1, swap2', swaps)
def test_RubikSmallGroup_word_eliminating_pair(swap1, swap2):

    rsg = RubikSmallGroup()

    p = Permutation().apply_cycle(swap1).apply_cycle(swap2)
    word = rsg.word_eliminating_pair(swap1, swap2)
    q = rsg.apply_word(word)
    assert (p * q).len() == 0
    assert (q * p).len() == 0
