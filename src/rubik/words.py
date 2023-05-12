from __future__ import annotations
from itertools import combinations_with_replacement, product
from math import comb, factorial
from pathlib import Path
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


def instruction(ws: str):
    for w in ws:
        print(w)
        input()
    print('DONE!')


class CycleLexica:
    """ База соответствия циклов длины n и слов из которых этот цикл можно
    получить."""

    def __init__(self, dim: int):
        self.dim = dim
        self.vocab = dict()

    def add(self, *sensorship: str):
        """ Добавить новые циклы в базу. """
        for w in sensorship:
            p = word(w)
            cycle = self.get_word_by_cycle(p)
            self.vocab[cycle] = w

    def get_word_by_cycle(self, p: Permutation) -> tuple:
        """ Достать слово цикла из базы. """
        cycles = p.cycles()
        if len(cycles) > 1 or len(cycles[0]) != self.dim:
            raise ValueError(f"Permuation {p} include more then 1 cycle.")
        mc = min(cycles[0])
        mi = [i for i, c in enumerate(cycles[0]) if c == mc][0]
        return tuple(cycles[0][mi:] + cycles[0][:mi])

    @classmethod
    def load(cls, path: Path) -> CycleLexica:
        """ Загрузить лексику из файла. """

        ws = []
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                ws.append(line)

        if len(ws) == 0:
            raise TypeError(f"File {path} doesn't have any line.")

        dim = word(ws[0]).len()

        cl = CycleLexica(dim)
        cl.add(*ws)
        return cl

    def save(self, path: Path):
        """ Сохранить лексику в файл. """
        words_list = self.vocab.values()
        with open(path, 'w') as f:
            f.write('\n'.join(words_list))

    def permutation2word(p: Permutation) -> str:
        pairs = p.swaps()
        
        def take_triplet(swap_list) -> Tuple[List[Swap], List[int]]:
            pass
            
            

if __name__ == '__main__':

    # for w, p in tqdm(words_gen(5, 0), total=total_words_volume(5, 0)):

    #     if p.len() == 0:
    #         print(w, p)

    #     # if p.deg() % 5 == 0:
    #     #     print('5', w, p)
    #     # if p.deg() % 7 == 0:
    #     #     print('7', w, p)

    dim = 3
    where_to_save = Path('lexica_3dim')
    cl = CycleLexica(dim)

    for w1, p1 in tqdm(words_gen(5, 2), total=total_words_volume(5, 2)):
        if p1.deg() % 7 != 0:
            continue
        for w2, p2 in words_gen(5, 2):
            if p2.deg() % 5 != 0:
                continue

            p = p1 * p2
            q = p ** 2

            if q.len() == dim:
                cl.add(w1 + w2 + w1 + w2)

            p = p2 * p1
            q = p ** 2
            if q.len() == dim:
                cl.add(w2 + w1 + w2 + w1)

    cl.save(where_to_save)
