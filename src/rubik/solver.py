from typing import List, Optional, Tuple

from rubik.permutation import Permutation
from rubik.words import ACT


Swap = Tuple[int, int]
Triplet = Tuple[int, int, int]
SwapL = List[Swap]
# TripletL = List[Triplet]


def separate_swaps(p: Permutation) -> Tuple[SwapL, SwapL]:
    """ Разделить список перестановок на два отдельных списка с сохранением
    порядка. Перестановки разделяются на перестановки на подгруппе вершин и
    перестановки на подгруппе ребер."""

    # TODO
    VERTEX = set([i for i in range(1, 9)])
    vertex, edge = [], []
    for xs in p.swaps():
        if xs[0] in VERTEX:
            vertex.append(xs)
        else:
            edge.append(xs)

    return vertex, edge


def swaps_to_triplets(swaps_list: List[Swap]) -> List[Triplet]:
    """ Преобразовать список перестановок в список триплетов, с сохранением
    порядка следования."""

    n = len(swaps_list)
    assert len(swaps_list) % 2 == 0
    res = []
    for i in range(n // 2):
        a, b = swaps_list[2 * i]
        c, d = swaps_list[2 * i + 1]

        if a not in [c, d] and b not in [c, d]:
            # (a b) (c d) = (a b) (b c) (b c) (c d) = (a c b) (b d c)
            res.append((a, c, b))
            res.append((b, d, c))
            continue

        if a in [c, d] and b in [c, d]:
            continue

        if a == c:
            # (a b) (a d) = (a b d)
            res.append((a, b, d))
        elif a == d:
            # (a b) (c a) = (a b c)
            res.append((a, b, d))
        elif b == c:
            # (a b) (b d) = (a d b)
            res.append((a, d, b))
        else:
            # (a b) (c b) = (a c b)
            res.append((a, c, b))

    return res


def permutation_triplets(p: Permutation) -> Optional[List[Triplet]]:
    """ Представить перестановку на кубике рубика в виде произведение циклов
    длины 3. Если перестановки не существует, функция вернет None."""

    # Любая перестановка над кубиком рубика будет четной потому, что вращения
    # действуют одновременно на две погруппы в каждой из которых создают
    # нечетные перестановки.

    swaps = p.swaps()
    dim = len(swaps) // 2
    q = p if dim % 2 == 0 else p * ACT['O']

    # Перестановка q на каждой из подгрупп четная.
    vertex, edge = separate_swaps(q)
    assert len(vertex) % 2 == 0
    assert len(edge) % 2 == 0

    vertex_triplets = []
    for i in range(len(vertex) // 2):
        a, b = vertex[2 * i]
        c, d = vertex[2 * i + 1]
        if a not in [c, d] and b not in [c, d]:
            vertex_triplets.append()
