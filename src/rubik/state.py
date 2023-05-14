from __future__ import annotations
from typing import Optional
from pathlib import Path

from rubik.permutation import Permutation
from rubik.coloring import Vector, ColoringCell, Color, rotate, cell


class Rubik:
    """ Состояние кубика рубика. """
    cells = [
        # This is solid ordering for convenient handle checking.
        # Малая подргуппа
        # верхняя крышка
        Vector(1, 1, 1),
        Vector(1, -1, 1),
        Vector(-1, -1, 1),
        Vector(-1, 1, 1),

        # нижняя крышка
        Vector(1, 1, -1),
        Vector(1, -1, -1),
        Vector(-1, -1, -1),
        Vector(-1, 1, -1),

        # Большая подргуппа
        Vector(1, 0, 1),    # 9
        Vector(0, -1, 1),   # 10
        Vector(-1, 0, 1),   # 11
        Vector(0, 1, 1),    # 12

        Vector(1, 1, 0),    # 13
        Vector(1, -1, 0),   # 14
        Vector(-1, -1, 0),  # 15
        Vector(-1, 1, 0),   # 16

        Vector(1, 0, -1),   # 17
        Vector(0, -1, -1),  # 18
        Vector(-1, 0, -1),  # 19
        Vector(0, 1, -1),   # 20
    ]

    def __init__(self, coloring: Optional[ColoringCell] = None):
        self.cells_index = {cell: i + 1 for i, cell in enumerate(self.cells)}
        self._coloring = {cell: cell for cell in self.cells}
        if coloring is not None:
            self.coloring = coloring

    @property
    def coloring(self) -> ColoringCell:
        """ Раскраска. """
        return self._coloring

    @coloring.setter
    def coloring(self, coloring: ColoringCell) -> None:
        """ Раскраска. """
        for cell_a, cell_b in coloring.items():
            self._coloring[cell_a] = cell_b

    def permutation(
        self,
    ) -> Permutation:
        """ Map coloring to permutation. """

        perm = dict()
        for a, b in self.coloring.items():
            if a == b:
                continue
            i = self.cells_index[a]
            j = self.cells_index[b]
            perm[j] = i

        return Permutation(perm)

    def act(self, color: Color) -> Rubik:
        """ Применить элементарное действие на стейте. """
        coloring = dict()
        for v, c in self.coloring.items():
            d = rotate(v, color)
            coloring[d] = c
        self.coloring = coloring
        return self

    def apply(self, word: str):
        """ Применить последовательность действий. Действия будут применяться
        слева направо. """
        for w in word:
            if w == ' ':
                continue
            color = Color.__members__.get(w)
            if color is None:
                raise ValueError(f"Unknown color in the word {word}.")

            self.act(color)

    @classmethod
    def load(cls, path: Path) -> Rubik:
        """ Загрузить состояние из файла. """
        coloring: ColoringCell = dict()
        with open(path, 'r') as f:
            for line in f:
                x, y, z, color = line.split()
                cell_a = Vector(int(x), int(y), int(z))
                cell_b = cell(color)
                coloring[cell_a] = cell_b
        return Rubik(coloring)

    def save(self, path: Path):
        # TODO
        pass
