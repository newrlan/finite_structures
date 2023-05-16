from __future__ import annotations
from itertools import combinations, combinations_with_replacement, product
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


class Cycle3Lexica:
    def __init__(self, path: Optional[Path] = None):
        self.vocab: dict[Tuple[int, int, int], str] = dict()
        if path is not None:
            self = self.load(path)

    def add(self, *word_list: str, recover=False):
        """ Добавить новое слово в лексику. Флаг recover указывает нужно ли
        перезаписать (использовать новое к уже существующему триплету) слово
        если оно уже есть в лексике. Если флаг выставлен в recover=False, то из
        двух версий будет выбрана короткая. """

        for ws in word_list:
            p = word(ws)
            cycle = p.cycles()
            assert len(cycle) == 1
            assert len(cycle[0]) == 3
            triplet = self._standart_triplet(cycle[0])

            if self.vocab.get(triplet) is None:
                self.vocab[triplet] = ws
                continue

            # Процедура проверки, что новое слово для триплета короче имеющегося
            if recover:
                self.vocab[triplet] = ws
                continue

            if len(self.vocab.get(triplet, ws)) <= len(ws):
                continue

            self.vocab[triplet] = ws

    @staticmethod
    def _standart_triplet(tr: Tuple[int, int, int]) -> Tuple[int, int, int]:
            a, b, c = tr
            return min((a, b, c), (b, c, a), (c, a, b))

    def get(self, tr: Tuple[int, int, int]) -> Optional[str]:
        tr_ = self._standart_triplet(tr)
        return self.vocab.get(tr_)
        
    @classmethod
    def load(cls, path: Path) -> Cycle3Lexica:
        """ Загрузить лексику из файла. """

        ws = []
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                ws.append(line)

        if len(ws) == 0:
            raise TypeError(f"File {path} doesn't have any line.")

        cl = Cycle3Lexica()
        cl.add(*ws)
        return cl

    def save(self, path: Path):
        """ Сохранить лексику в файл. """
        words_list = self.vocab.values()
        with open(path, 'w') as f:
            f.write('\n'.join(words_list))

    def bruteforse(self):
        deg = 5
        uniq_act = 2
        gen = words_gen(deg, uniq_act)
        deg_7_words = dict()
        deg_5_words = dict()

        for w, p in tqdm(gen, total=total_words_volume(deg, uniq_act)):
            if p.deg() % 7 == 0:
                deg_7_words[w] = p
            if p.deg() % 5 == 0:
                deg_5_words[w] = p

        t_pairs = len(deg_7_words) * len(deg_5_words)
        for w1, w2 in tqdm(product(deg_7_words, deg_5_words), total=t_pairs):
            p1 = deg_7_words[w1]
            p2 = deg_5_words[w2]

            q = (p1 * p2) ** 2
            if q.len() == 3:
                self.add(w1 + w2 + w1 + w2)

            q = (p2 * p1) ** 2
            if q.len() == 3:
                self.add(w2 + w1 + w2 + w1)

        self.fill_unknown_triplets()

    def fill_unknown_triplets(self):
        """Посчитать все произведения 3-циклов и те, что дают новые 3-циклы
        добавить в словарь."""

        addition_words = []
        for pair1, pair2 in product(self.vocab.items(), self.vocab.items()):
            tr1, w1 = pair1
            tr2, w2 = pair2

            p1 = Permutation().apply_cycle(tr1)
            p2 = Permutation().apply_cycle(tr2)

            q = p1 * p2
            if q.len() == 3:
                wq = w1 + w2
                addition_words.append(wq)
        self.add(*addition_words)

    def uncovered_triplets(self) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
        vertex = []
        for a, b, c in combinations(range(1, 8 + 1), 3):
            if (a, b, c) not in self.vocab:
                vertex.append((a, b, c))
            if (a, c, b) not in self.vocab:
                vertex.append((a, b, c))

        edge = []
        for a, b, c in combinations(range(9, 20 + 1), 3):
            if (a, b, c) not in self.vocab:
                edge.append((a, b, c))
            if (a, c, b) not in self.vocab:
                edge.append((a, b, c))

        return vertex, edge


if __name__ == '__main__':

    cl = Cycle3Lexica.load(Path('lexica/3dim_full'))
    v, e = cl.uncovered_triplets()
    print('uncovered', v, e)
