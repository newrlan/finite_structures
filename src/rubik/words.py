from collections.abc import Set
from itertools import combinations_with_replacement, product
from math import comb, factorial
from typing import Generator, List, Optional, Tuple

from tqdm import tqdm
from rubik.permutation import Permutation
from rubik.coloring import Color
from rubik.state import Rubik

ACT = {
    # Элементарные действия над кубиком Рубика
    'O': Rubik().act(Color.O).permutation(),
    'B': Rubik().act(Color.B).permutation(),
    'Y': Rubik().act(Color.Y).permutation(),
    'W': Rubik().act(Color.W).permutation(),
    'G': Rubik().act(Color.G).permutation(),
    'R': Rubik().act(Color.R).permutation(),
}


def word(ws: str) -> Permutation:
    """ Конвертировать слово в перестановку. """
    p = Permutation()
    for w in ws:
        p *= ACT[w.upper()]
    return p


def dim(xs, n) -> List[str]:
    """ Составить всевозможные комбинации из n элементов на основе множества
    xs."""

    return [''.join(arr) for arr in product(*[xs for _ in range(n)])]


def _combination_of_splits(n: int, k: int) -> int:
    cum = 0
    for arr in combinations_with_replacement([i for i in range(k)], n-k):
        loc_cum = factorial(n)
        for i in range(k):
            ki = 1 + len([x for x in arr if x == i])
            loc_cum //= factorial(ki)
        cum += loc_cum
    return cum


def words_gen(n: int, k: int = 2) -> \
        Generator[Tuple[str, Permutation], None, None]:
    """ Генератор всевозможных слов длины n в которых участвует k и более
    различных элементов. Возвращает пару (слово, перестановка). """

    for arr in product(*[ACT for _ in range(n)]):
        w = ''.join(arr)
        if len(set(w)) < k:
            continue
        p = word(w)
        yield (w, p)


def total_words_volume(n: int, k: int) -> int:
    """ Вычислить количество слов порождаемых генератором words_gen. """

    if k > 6:
        return 0

    total = 6 ** n
    for i in range(1, k):
        total -= _combination_of_splits(n, i) * comb(6, i)

    return total


def words_dim(n: int, k: int = 2) -> dict[str, Permutation]:
    res = dict()
    for w in dim(ACT, n):
        if len(set(w)) <= k:
            continue
        p = word(w)
        res[w] = p
    return res


def instruction(ws: str):
    for w in ws:
        print(w)
        input()
    print('DONE!')


if __name__ == '__main__':

    num = 0
    for _ in words_gen(3, 2):
        num += 1
    print(num)
    print(total_words_volume(3, 2))
