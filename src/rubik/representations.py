from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional
from termcolor import colored

from rubik.coloring import Color
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

    def __init__(self, path: Optional[Path] = None):

        self.state = {key: key[0] for key in self.codes}

    @staticmethod
    def _square_prepare(square: List[List[str]]) -> dict[str, str]:
        """ Прочитать раскраску квадрата. """
        c = square[1][1]    # цвет центральной точки квадрата
        assert c.upper() in Color.__members__, f"Undefined color {c.upper()}."
        res = dict()
        line = sum(square, [])
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
            squares.append(coloring[i+1:i+4])

        add_msg = " Please, check orientation."
        assert squares[0][1][1].lower() == coloring[0][2].lower, error_msg + add_msg
        assert squares[1][1][1].lower() == coloring[0][0].lower, error_msg + add_msg
        assert squares[3][1][1].lower() == coloring[0][1].lower, error_msg + add_msg

        # В следующих переменных содержатся оппозиционные цвета. Первый цвет в
        # паре, цвет положительного направления, второй - отрицательного.

        self._color_Ox = (coloring[0][0], squares[1][1][1])
        self._color_Oy = (coloring[0][1], squares[5][1][1])
        self._color_Oz = (coloring[0][2], squares[2][1][1])

        state = dict()
        for sqr in squares:
            state = {**state, **self._square_prepare(sqr)}
        self.state = state

    def _take_square(self, color: Color):
        square = {key: value for key, value in self.state.items()
                  if key[0] == color.name}
        return square

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
        val = self.state[key]
        return colored('栗', color[val])

    def _show_face(self, k: str) -> List[str]:
        if k not in self.colors:
            raise ValueError(f'Key {k} must be in list {self.colors}')

        res = []
        for j in range(3):
            line = ''.join([self._show_label(f'{k}{i+3*j}') for i in [1, 2, 3]])
            res.append(line)

        return res
        # return '\n'.join(res)

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

        



        

    # def show_square(self, color: Color):
    # def show_square(self):
    #     # square = self._take_square(color)
    #     # square.insert(color.name, 4)
    #     square = [['O', 'O', 'Y'],['O', 'O', 'Y'],['O', 'O', 'Y']]
    #     txt = ''
    #     for x in 
    #     txt = colored('栗', 'red') + colored('栗', 'green') + colored('栗', 'white') + \
    #             ' ' + colored('栗', 'red') + colored('栗', 'green') + colored('栗', 'white') 
    #     print(' ' + txt, '\n', txt, '\n', txt)


    @classmethod
    def load(cls, path: Path):
        pass

    def permutation(self):
        pass

    # @classmethod
    # def load(cls, path: Path) -> Rubik:
    #     """ Загрузить состояние из файла. """
    #     coloring: ColoringCell = dict()
    #     with open(path, 'r') as f:
    #         for line in f:
    #             x, y, z, color = line.split()
    #             cell_a = Vector(int(x), int(y), int(z))
    #             cell_b = cell(color)
    #             coloring[cell_a] = cell_b
    #     return Rubik(coloring)


if __name__ == '__main__':
    cl = InvoluteRepresentation()
    cl.show()
