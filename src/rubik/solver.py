from pathlib import Path
from typing import List, Optional, Tuple

from rubik.permutation import Permutation
from rubik.state import Rubik
from rubik.words import ACT, CycleLexica


Swap = Tuple[int, int]
Triplet = Tuple[int, int, int]
SwapL = List[Swap]


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
    assert len(swaps_list) % 2 != 0, "Only even permutations can be decompose on triplets."
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


def permutation_triplets(p: Permutation) -> List[Triplet]:
    """ Представить перестановку на кубике рубика в виде произведение циклов
    длины 3. Если перестановки не существует, функция вернет None."""

    # Любая перестановка над кубиком рубика будет четной потому, что вращения
    # действуют одновременно на две погруппы в каждой из которых создают
    # нечетные перестановки. Однако, поскольку разложить на триплеты мы можем
    # только четные перестановки, и перестановки не могут выводить из подгруппы,
    # итоговая перестановка должна быть кратна 4.

    # Перестановка q на каждой из подгрупп четная.
    vertex, edge = separate_swaps(p)
    v_triplets = swaps_to_triplets(vertex)
    e_triplets = swaps_to_triplets(edge)

    return v_triplets + e_triplets


if __name__ == '__main__':
    cl = CycleLexica.load(Path('lexica/lexica_3dim'))
    rubik = Rubik.load(Path('src/rubik/state.txt'))
    p = rubik.permutation()  #.apply_cycle((18, 20))
    print('p', p)
    if len(p.swaps()) % 4 != 0:
        p = p * ACT['O']
    tr_list = permutation_triplets(p)
    print(tr_list)
    for tr in tr_list:
        q = Permutation().apply_cycle(tr)
        i = cl.get_word_by_cycle(q)
        print(cl.vocab[i])

    # for tr, ws in cl.vocab.items():
    #     if 9 in tr and 17 in tr and 15 in tr:
    #         print(tr, '\t', ws)

    # (9 15 17) (9 15 17) = (9 17 15)
