from collections.abc import Set
from itertools import product
from math import comb, factorial
from typing import Generator, List, Optional, Tuple

from tqdm import tqdm
from rubik.permutation import Permutation
from rubik.coloring import Color
from rubik.state import Rubik

ACT = {
    # Элементарные действия над кубиком рубика
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

    def P(n, s):
        return comb(6, s) * (s ** (n - s))

    return sum([P(n, s) for s in range(k, 6 + 1)])

    # c = comb(6, k)      # места где расположить неповторящиеся элементы
    # c *= factorial(k)   # комбинации перестановок неповторяющихся элементов
    # c *= 6 ** (n - k)   # в оставшихся местах произвольные элементы
    # return c


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

                if w1 != w2 and p1 == p2:
                    if len(set(w1 + w2)) > m:
                        res.append(w1 + w2)
                        res.append(w2 + w1)
                        print(w1, '=', w2)
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

                if p1 == p2:
                    if len(set(w1 + w2)) > m:
                        res.append(w1 + w2)
                        res.append(w2 + w1)
                        print(w1, '=', w2)

    return res


def brutforce_compare(n, k, m=1):
    wd_n = words_gen(n, m)
    wd_k = words_gen(k, 1)
    for w1, p1 in tqdm(wd_n, total=total_words_volume(n, m)):
        for w2, p2 in wd_k:
            if p1 == p2:
                # if len(set(w1 + w2)) < m:
                #     continue
                print(w1, '=', w2)


def instruction(ws: str):
    for w in ws:
        print(w)
        input()
    print('DONE!')


if __name__ == '__main__':

    # for w, p in tqdm(words_gen(6, 3), total=total_words_volume(6, 3)):
    #     if p.deg() % 3 == 0:
    #         print(w, p)
    # brute_force_trivial_words(9, 2)
    # brutforce_compare(3, 2, 1)
    # for w in tqdm(words_gen(8, 2), total=total):
    #     continue
    #     print(w)
    kand = [
     (7, 3),
     ]
    for n, k in kand:
        m = len([1 for _ in tqdm(words_gen(n, k))])
        print(n, k, m, '\n')
