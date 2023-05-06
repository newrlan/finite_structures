from collections.abc import Set
from itertools import product
from typing import List, Optional

from tqdm import tqdm
from rubik.permutation import Permutation
from rubik.coloring import Color
from rubik.state import Rubik

VERTEX_GEN_PERMUTATION = {
    'O': Rubik().act(Color.O).permutation(),
    'B': Rubik().act(Color.B).permutation(),
    'Y': Rubik().act(Color.Y).permutation(),
    'W': Rubik().act(Color.W).permutation(),
    'G': Rubik().act(Color.G).permutation(),
    'R': Rubik().act(Color.R).permutation(),
}

ACT = {
    ## # deg 3
    ## 'O': VERTEX_GEN_PERMUTATION['O'] ** 3,
    ## 'B': VERTEX_GEN_PERMUTATION['B'] ** 3,
    ## 'Y': VERTEX_GEN_PERMUTATION['Y'] ** 3,
    ## 'W': VERTEX_GEN_PERMUTATION['W'] ** 3,
    ## 'G': VERTEX_GEN_PERMUTATION['G'] ** 3,
    ## 'R': VERTEX_GEN_PERMUTATION['R'] ** 3,
    # deg 1
    'o': VERTEX_GEN_PERMUTATION['O'],
    'b': VERTEX_GEN_PERMUTATION['B'],
    'y': VERTEX_GEN_PERMUTATION['Y'],
    'w': VERTEX_GEN_PERMUTATION['W'],
    'g': VERTEX_GEN_PERMUTATION['G'],
    'r': VERTEX_GEN_PERMUTATION['R'],
}


def word(ws: str) -> Permutation:
    p = Permutation()
    for w in ws:
        p *= ACT[w]
    return p


def dim(xs, n) -> List[str]:
    return [''.join(arr) for arr in product(*[xs for _ in range(n)])]


def words_dim(n: int, k: int = 2) -> dict[str, Permutation]:
    res = dict()
    for w in dim(ACT, n):
        if len(set(w)) <= k:
            continue
        p = word(w)
        res[w] = p
    return res


def brute_force_trivial_words(n: int, m: int = 2) -> List[str]:
    """ Отобрать все тривиальные слова, среди слов длины n. Минимальное
    количество уникальных символов в слове - m. """

    res = []

    if n % 2 == 0:
        wd_n = words_dim(n // 2, m)
        key = [v for v in wd_n]
        len_key = len(key)
        for i, w1 in tqdm(enumerate(key), total=len_key):
            p1 = wd_n[w1]
            for w2 in key[i:]:
                p2 = wd_n[w2]
                if len(set(w1 + w2)) <= m:
                    continue
                p = p1 * p2
                if p.len() == 0:
                    if len(set(w1 + w2)) > m:
                        res.append(w1 + w2)
                        res.append(w2 + w1)
                        print(w1, w2)
    else:
        wd_n = words_dim((n + 1) // 2, m)
        wd_k = words_dim(n // 2, m)
        for w1, p1 in tqdm(wd_n.items()):
            for w2, p2 in wd_k.items():
                if len(set(w1 + w2)) <= m:
                    continue
                p = p1 * p2
                if p.len() == 0:
                    if len(set(w1 + w2)) > m:
                        res.append(w1 + w2)
                        res.append(w2 + w1)
                        print(w1, w2)

    return res


def instruction(ws: str):
    for w in ws:
        print(w)
        input()
    print('DONE!')


if __name__ == '__main__':

    # brute_force_trivial_words(12, 3)
    w = 'oywgbrowygbr'
    p = word(w)
    print(p)
    # instruction(w)
    print(ACT['o'])
    print(ACT['b'])
    print(ACT['y'])
    print(ACT['g'])
    print(ACT['w'])
    print(ACT['r'])
