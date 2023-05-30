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

    colors = [col.name.upper() for col in Color]
    codes = [f'{c}{n}' for n in range(1, 9 + 1)
             for c in [col.name.upper() for col in Color]]

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

    def __init__(self):
        self.state = {key: key for key in self.codes}

    @staticmethod
    def _square_prepare(square: List[List[str]]) -> dict[str, str]:
        """ Прочитать раскраску квадрата. """
        c = square[1][1]    # цвет центральной точки квадрата
        assert c.upper() in Color.__members__, f"Undefined color {c.upper()}."
        res = dict()
        line = sum([list(x) for x in square], [])
        for i, col in enumerate(line):
            assert col.upper() in Color.__members__, f"Undefined color {col.upper()}"
            res[f'{c}{i+1}'] = col

        return res

    def prepare(self, coloring):
        """ Переводит раскраску к удобному виду. """

        error_msg = "Incorrect coloring representation."
        assert len(coloring) == 19, error_msg

        # В первой строке лежат координаты векторов Ox, Oy, Oz (положительные направления)
        squares = []
        for i in range(6):
            squares.append(coloring[3 * i + 1:3 * i + 4])

        add_msg = " Please, check orientation."
        assert squares[0][1][1].lower() == coloring[0][2].lower(), error_msg + add_msg
        assert squares[1][1][1].lower() == coloring[0][0].lower(), error_msg + add_msg
        assert squares[3][1][1].lower() == coloring[0][1].lower(), error_msg + add_msg

        # В следующих переменных содержатся оппозиционные цвета. Первый цвет в
        # паре, цвет положительного направления, второй - отрицательного.

        self._color_Ox = (coloring[0][0], squares[1][1][1])
        self._color_Oy = (coloring[0][1], squares[5][1][1])
        self._color_Oz = (coloring[0][2], squares[2][1][1])

        state = dict()
        for sqr in squares:
            state = {**state, **self._square_prepare(sqr)}

        state = self._index_state(state)
        self.state = state

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
    def load(cls, path: Path):
        with open(path, 'r') as f:
            coloring = [line.replace('\n', '') for line in f if line != '\n']
            self = cls()
            self.prepare(coloring)
            return self

    def permutation(self):
        indexis = {key: i for i, key in enumerate(self.codes)}
        perm = dict()
        for key, val in self.state.items():
            i = indexis[key]
            j = indexis[val]
            perm[j] = i

        return Permutation(perm)

    @classmethod
    def _vertex_state_permutation(cls, state: dict[str, str]) -> Permutation:

        def name(xs):
            abs = [x[0] for x in xs]
            abs.sort()
            return ''.join(abs)

        tr_names = {name(tr): i for i, tr in enumerate(cls._vertex)}

        perm_dict = dict()
        for tr in cls._vertex:
            who = tr_names[name([state.get(x, x) for x in tr])]
            where = tr_names[name(tr)]
            perm_dict[who] = where

        return Permutation(perm_dict)

    @classmethod
    def _edges_state_permutation(cls, state: dict[str, str]) -> Permutation:
        
        def name(xs):
            abs = [x[0] for x in xs]
            abs.sort()
            return ''.join(abs)

        tr_names = {name(tr): i for i, tr in enumerate(cls._edges)}

        perm_dict = dict()
        for tr in cls._edges:
            who = tr_names[name([state.get(x, x) for x in tr])]
            where = tr_names[name(tr)]
            perm_dict[who] = where

        return Permutation(perm_dict)

    def _index_state(self, state: dict[str, str]) -> dict[str, str]:
        new_state = {f'{c}5': f'{c}5' for c in self.colors}
        pv = self._vertex_state_permutation(state)
        for i, tr in enumerate(self._vertex):
            j = pv.apply(i)
            image = {c[0]: c for c in self._vertex[j]}
            for c in tr:
                color = state[c]
                new_state[c] = image[color]

        pv = self._edges_state_permutation(state)
        for i, tr in enumerate(self._edges):
            j = pv.apply(i)
            image = {c[0]: c for c in self._edges[j]}
            for c in tr:
                color = state[c]
                new_state[c] = image[color]

        return new_state


if __name__ == '__main__':
    cl = InvoluteRepresentation.load(Path('src/rubik/state_inv.txt'))
    cl.show()
    print(cl.state)
    print(cl.permutation())
    cycles = cl.permutation().cycles()
    for cyc in cycles:
        line = ' '.join([cl.codes[i] for i in cyc])
        print(line)

