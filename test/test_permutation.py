from rubik.permutation import Permutation#, RubikSmallGroup
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


def test_permutation___eq__():
    p = Permutation({1: 2, 2: 1})
    q = Permutation({1: 2, 2: 1, 3: 4, 4: 5, 5: 3})
    s = Permutation({3: 4, 4: 5, 5: 3})

    assert p != q
    assert p != s
    assert q != s
    assert q == p * s


def test_permutation_apply_cycle():
    q = Permutation().apply_cycle(['R4', 'R8', 'G5', 'F1', 'C4'])

    perm_dict = {'R4': 'R8', 'R8': 'G5', 'G5': 'F1', 'F1': 'C4', 'C4': 'R4'}
    p = Permutation(perm_dict)
    assert p == q


def test_permutation___repr__():
    p = Permutation().apply_cycle(['R4', 'G8', 'F5'], ['O1', 'Y2'])
    line = str(p)
    assert line == '(R4 G8 F5) (O1 Y2)' or \
        line == '(G8 F5 R4) (O1 Y2)' or \
        line == '(F5 R4 G8) (O1 Y2)' or \
        line == '(R4 G8 F5) (Y2 O1)' or \
        line == '(G8 F5 R4) (Y2 O1)' or \
        line == '(F5 R4 G8) (Y2 O1)' or \
        line == '(O1 Y2) (R4 G8 F5)' or \
        line == '(O1 Y2) (G8 F5 R4)' or \
        line == '(O1 Y2) (F5 R4 G8)' or \
        line == '(Y2 O1) (R4 G8 F5)' or \
        line == '(Y2 O1) (G8 F5 R4)' or \
        line == '(Y2 O1) (F5 R4 G8)'


def test_permutation_cycle():

    p = Permutation()
    q = p.apply_cycle([1, 3, 2, 4]).apply_cycle([5, 6])

    cycle = q.cycles()
    assert len(cycle) == 2
    assert cycle[0] == [1, 3, 2, 4]
    assert cycle[1] == [5, 6]


# swaps = [
#     ((1, 3), (2, 4)),
#     ((2, 3), (2, 4)),
#     ((1, 2), (2, 4)),
#     ((1, 2), (4, 2)),
#     ((1, 4), (1, 4)),
#     ((2, 4), (2, 3)),
#     ((2, 6), (2, 5)),
# ]
# 
# 
# @pytest.mark.parametrize('swap1, swap2', swaps)
# def test_RubikSmallGroup_word_eliminating_pair(swap1, swap2):
# 
#     rsg = RubikSmallGroup()
# 
#     p = Permutation().apply_cycle(swap1).apply_cycle(swap2)
#     word = rsg.word_eliminating_pair(swap1, swap2)
#     q = rsg.word2permutation(word)
#     assert (p * q).len() == 0
#     assert (q * p).len() == 0
# 
# 
# permutations = [
#     Permutation()\
#         .apply_cycle((1, 2))\
#         .apply_cycle((1, 3))\
#         .apply_cycle((2, 3))\
#         .apply_cycle((3, 4)),
#     Permutation()\
#         .apply_cycle((1, 2))\
#         .apply_cycle((1, 3))\
#         .apply_cycle((2, 3)),
#     Permutation()\
#         .apply_cycle((1, 2))\
#         .apply_cycle((3, 4)),
#     Permutation().apply_cycle([2, 6, 5, 4, 3]),
#     Permutation().apply_cycle([2, 6, 5, 4, 3]).apply_cycle((1, 8)),
#     Permutation()
# ]
# 
# 
# @pytest.mark.parametrize('p', permutations)
# def test_RubikSmallGroup_permutation2word(p):
#     rsg = RubikSmallGroup()
#     word = rsg.permutation2word(p)
#     q = rsg.word2permutation(word)
#     assert (p * q).len() == 0
#     assert (q * p).len() == 0
