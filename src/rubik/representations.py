from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional
from termcolor import colored

from rubik.coloring import Color, Vector
from rubik.permutation import Permutation


class Representation(ABC):
    """ Интерфейс класса кодировки кубика Рубика. """

    @abstractmethod
    def permutation(self) -> Permutation:
        pass

    @classmethod
    @abstractmethod
    def load(cls, path: Path) -> Representation:
        pass


class InvoluteRepresentation(Representation):

    """ Чтобы задать представление кубика Рубика в виде развертки достаточно
    прописать цвета всех его граней, но сделать это нужно в определенной
    последовательности. 

    Первая строка, записываются три цвета (без пробела):
        1. Цвет который лежит на оси X
        2. Цвет который лежит на оси Y
        3. Цвет который лежит на оси Z

    Далее 18 строк в каждой из которых по три символа. Строки группируются по
    три, каждая группа строк описывает одну грань кубика Рубика. В каком
    порядке расположить грани в представлении:
        - Первая грань с центром в O
        - Вторая грань с центром в B
        - Третья грань с центром в R
    Обратите внимание, что при кодировании, первая строка на синей грани должна
    касаться последней строки на оранжевой грани. Такое требование и для
    красной и синей граней.

    Если вы выбрали другие грани, то это последование кручение кубика
    относительно оси Y. Только заднюю грань мы пока в это описание не включаем,
    оно позже.

    Далее грани описываются в таком порядке:
        - Четвертая грань с центром в Y
        - Пятая грань с центром в G (задняя сторона)
        - Шестая грань с центром в R

    Если у вас выбраны другие цвета в качестве оснований, то последняя тройка 
    описывается поворотом вектора (0, 1, 0) вокруг оси Oz, сперва в вектор 
    (-1, 0, 0), а потом в вектор (0, -1, 0).

    Первая строка в этом описании как раз нужна для того, чтобы определить
    цвета ваших осей и дополнительно проверить кодировку.

    Note: Пустые строки в файле будут игнорироваться.
    """

    # colors = [col.name.upper() for col in Color]
    colors = ['O', 'B', 'R', 'Y', 'G', 'W']

    _vertex = [
        # Upper face
        ('B3', 'O9', 'Y3'),
        ('W9', 'B1', 'O7'),
        ('G9', 'W3', 'O1'),
        ('O3', 'Y9', 'G3'),
        # Down face
        ('B9', 'R3', 'Y1'),
        ('W7', 'R1', 'B7'),
        ('G7', 'W1', 'R7'),
        ('R9', 'G1', 'Y7'),
    ]

    _edges = [
        ('G2', 'Y8'),
        ('G6', 'O2'),
        ('G4', 'R8'),
        ('G8', 'W2'),
        ('W4', 'R4'),
        ('W6', 'O4'),
        ('B8', 'R2'),
        ('B2', 'O8'),
        ('W8', 'B4'),
        ('B6', 'Y2'),
        ('Y4', 'R6'),
        ('Y6', 'O6'),
    ]

    _actions = {
        "O": Permutation().apply_cycle(('O1', 'O3', 'O9', 'O7'),
                                       ('O2', 'O6', 'O8', 'O4'),
                                       ('B3', 'W9', 'G9', 'Y9'),
                                       ('B2', 'W6', 'G6', 'Y6'),
                                       ('B1', 'W3', 'G3', 'Y3')),
        "B": Permutation().apply_cycle(('B1', 'B3', 'B9', 'B7'),
                                       ('B2', 'B6', 'B8', 'B4'),
                                       ('O7', 'Y3', 'R3', 'W7'),
                                       ('O8', 'Y2', 'R2', 'W8'),
                                       ('O9', 'Y1', 'R1', 'W9')),
        "R": Permutation().apply_cycle(('R1', 'R3', 'R9', 'R7'),
                                       ('R2', 'R6', 'R8', 'R4'),
                                       ('B9', 'Y7', 'G7', 'W7'),
                                       ('B8', 'Y4', 'G4', 'W4'),
                                       ('B7', 'Y1', 'G1', 'W1')),
        "Y": Permutation().apply_cycle(('Y1', 'Y3', 'Y9', 'Y7'),
                                       ('Y2', 'Y6', 'Y8', 'Y4'),
                                       ('O9', 'G3', 'R9', 'B9'),
                                       ('O6', 'G2', 'R6', 'B6'),
                                       ('O3', 'G1', 'R3', 'B3')),
        "W": Permutation().apply_cycle(('W1', 'W3', 'W9', 'W7'),
                                       ('W2', 'W6', 'W8', 'W4'),
                                       ('O1', 'B1', 'R1', 'G7'),
                                       ('O4', 'B4', 'R4', 'G8'),
                                       ('O7', 'B7', 'R7', 'G9')),
        "G": Permutation().apply_cycle(('G1', 'G3', 'G9', 'G7'),
                                       ('G2', 'G6', 'G8', 'G4'),
                                       ('O1', 'W1', 'R7', 'Y9'),
                                       ('O2', 'W2', 'R8', 'Y8'),
                                       ('O3', 'W3', 'R9', 'Y7'))
    }

    @classmethod
    def standart_coloring(cls, group=True):
        """ Создать стандартную раскраску в сгруппированном виде тройками или
        простым списком."""

        res = []
        for c in cls.colors:
            for i in range(1, 9 + 1):
                res.append(c + str(i))

        if group:
            return [res[i:i+3] for i in range(0, len(res), 3)]

        return res

    def __init__(self):
        self.state = {key: key for key in self.standart_coloring(False)}

    def _show_label(self, key):
        color = {
            'W': 'white',
            'G': 'green',
            'R': 'red',
            'B': 'light_cyan',
            'Y': 'light_yellow',
            'O': 'yellow'
            # 'O': 'grey'
        }
        val = self.state[key][0]
        return colored('栗', color[val])

    def show(self):
        """ Показать раскраску на развертке куба.
        Схема как будут расположены квадраты развертки:
                    Oz
            -Ox -Oy Ox Oy
                   -Oz
        """

        i_matrix = [
            '                ╭───────╮     ',
            '                │ 123│     ',
            '                │ 456│     ',
            '                │ 789│     ',
            '╭───────┬───────┼───────┼───────╮',
            '│ 369│ 369│ 123│ 369│',
            '│ 258│ 258│ 456│ 258│',
            '│ 147│ 147│ 789│ 147│',
            '╰───────┴───────┼───────┼───────╯',
            '                │ 123│     ',
            '                │ 456│     ',
            '                │ 789│     ',
            '                ╰───────╯     ',
                ]

        c_matrix = [
            '                ╭───────╮     ',
            '                │ OOO│     ',
            '                │ OOO│     ',
            '                │ OOO│     ',
            '╭───────┬───────┼───────┼───────╮',
            '│ GGG│ WWW│ BBB│ YYY│',
            '│ GGG│ WWW│ BBB│ YYY│',
            '│ GGG│ WWW│ BBB│ YYY│',
            '╰───────┴───────┼───────┼───────╯',
            '                │ RRR│     ',
            '                │ RRR│     ',
            '                │ RRR│     ',
            '                ╰───────╯     ',
                ]

        res = []
        for c_line, i_line in zip(c_matrix, i_matrix):
            colored_line = ''
            for c, i in zip(c_line, i_line):
                try:
                    elem = self._show_label(c + i)
                except KeyError:
                    elem = c
                colored_line += elem

            res.append(colored_line)

        print('\n'.join(res))
        return None

    @classmethod
    def _set_color_index(cls, pre_coloring: dict[str, str]) -> dict[str, str]:
        """ Восстановить индексы вершин и ребер в предварительной раскраске. """

        obj_list = cls._vertex + cls._edges
        coloring = dict()
        obj_dict = dict()
        for tr in obj_list:
            name = [x[0] for x in tr]
            name.sort()
            name = tuple(name)
            obj_dict[name] = {x[0]: x for x in tr}

        for tr in obj_list:
            name = [pre_coloring[x] for x in tr]
            name.sort()
            name = tuple(name)
            assert name in obj_dict, f"For obj {tr} coloring has not valid case {name}."
            local_vertex_coloring = obj_dict[name]
            for x in tr:
                coloring[x] = local_vertex_coloring[pre_coloring[x]]

        for c in cls.colors:
            center = c + '5'
            coloring[center] = center

        return coloring

    @classmethod
    def load(cls, path: Path):
        """ Прочитать раскраску из файла. """

        with open(path, 'r') as f:
            lines = [line.replace('\n', '') for line in f if line != '\n']
            lines = lines[1:]

        pre_coloring = {}
        assert len(lines) == 18, f"Some problem with amount of lines in {path}."
        for coord, color in zip(cls.standart_coloring(), lines):
            assert len(coord) == len(color), f"There is mistake line in {path}."
            for x, y in zip(coord, color):
                pre_coloring[x] = y

        self = cls()
        self.state = cls._set_color_index(pre_coloring)
        return self

    def permutation(self):
        perm = dict()
        for key, val in self.state.items():
            perm[val] = key

        return Permutation(perm)

    def apply(self, word: str):

        perm = self.permutation()
        for w in word:
            q = self._actions.get(w.upper())
            perm *= q

        new_coloring = dict()
        for val in self.standart_coloring(group=False):
            key = perm.apply(val)
            new_coloring[key] = val

        self.state = new_coloring

    def state2tab(self) -> List[str]:
        """ Перевести состояние кубика в плоский формат в котором происходит
        чтение из файла."""

        tab = []
        for color in "OBRYGW":
            for index_line in [range(i, i+3) for i in range(1, 9, 3)]:
                line = []
                for i in index_line:
                    key = color + str(i)
                    val_color = self.state.get(key, key)[0]
                    line.append(val_color)

                tab.append(' '.join(line))

        return tab




if __name__ == '__main__':
    from time import sleep

    cl = InvoluteRepresentation.load(Path('test/state_action_BOW.txt'))

    for act in cl._actions:
        st = InvoluteRepresentation()
        st.apply(act)
        st.show()
