from rubik.permutation import Permutation
from rubik.rubik_group import RubikSmallGroup
import pytest



swaps = [
    ((1, 3), (2, 4)),
    ((2, 3), (2, 4)),
    ((1, 2), (2, 4)),
    ((1, 2), (4, 2)),
    ((1, 4), (1, 4)),
    ((2, 4), (2, 3)),
    ((2, 6), (2, 5)),
]


@pytest.mark.parametrize('swap1, swap2', swaps)
def test_RubikSmallGroup_word_eliminating_pair(swap1, swap2):

    rsg = RubikSmallGroup()

    p = Permutation().apply_cycle(swap1).apply_cycle(swap2)
    word = rsg.word_eliminating_pair(swap1, swap2)
    q = rsg.word2permutation(word)
    assert (p * q).len() == 0
    assert (q * p).len() == 0


permutations = [
    Permutation()\
        .apply_cycle((1, 2))\
        .apply_cycle((1, 3))\
        .apply_cycle((2, 3))\
        .apply_cycle((3, 4)),
    Permutation()\
        .apply_cycle((1, 2))\
        .apply_cycle((1, 3))\
        .apply_cycle((2, 3)),
    Permutation()\
        .apply_cycle((1, 2))\
        .apply_cycle((3, 4)),
    Permutation().apply_cycle([2, 6, 5, 4, 3]),
    Permutation().apply_cycle([2, 6, 5, 4, 3]).apply_cycle((1, 8)),
    Permutation()
]


@pytest.mark.parametrize('p', permutations)
def test_RubikSmallGroup_permutation2word(p):
    rsg = RubikSmallGroup()
    word = rsg.permutation2word(p)
    q = rsg.word2permutation(word)
    assert (p * q).len() == 0
    assert (q * p).len() == 0
