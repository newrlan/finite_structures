from __future__ import annotations
from typing import List, Optional, Any, Tuple, Type, TypeVar
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from rubik.permutation import Permutation
from rubik.coloring import Vector, ColoringCell, Color, rotate, cell


class Rubik:
    def __init__(self, coloring: Optional[ColoringCell] = None):
        self.cells = [
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
            Vector(1, 0, 1),
            Vector(1, 1, 0),
            Vector(1, 0, -1),
            Vector(1, -1, 0),

            Vector(-1, 0, 1),
            Vector(-1, 1, 0),
            Vector(-1, 0, -1),
            Vector(-1, -1, 0),

            Vector(0, 1, 1),
            Vector(0, 1, -1),
            Vector(0, -1, -1),
            Vector(0, -1, 1),
        ]
        self.cells_index = {cell: i + 1 for i, cell in enumerate(self.cells)}
        self.coloring = dict() if coloring is None else coloring

    @property
    def coloring(self) -> ColoringCell:
        return self._coloring

    @coloring.setter
    def coloring(self, coloring: ColoringCell) -> None:
        col = {cell: cell for cell in self.cells}
        for cell_a, cell_b in coloring.items():
            col[cell_a] = cell_b
        self._coloring = col

    def permutation(self, coloring: Optional[ColoringCell] = None) -> Permutation:
        """ Map coloring to permutation. """

        if coloring is None:
            coloring = self._coloring

        perm = dict()
        for a, b in coloring.items():
            if a == b:
                continue
            i = self.cells_index[a]
            j = self.cells_index[b]
            perm[j] = i

        # Permutation shows where color must be after action, but in
        # self.coloring we have color of cell after action. As a result key of
        # dictionary self.coloring is the destination of value.

        return Permutation(perm)

    def act(self, color: Color):
        self.coloring = {v: rotate(w, color) for v, w in self._coloring.items()}
        return self

    def apply(self, word: str):
        for w in word:
            color = Color.__members__.get(w)
            if color is None:
                raise ValueError(f"Unknown color in word {word}.")

            self.act(color)

    @classmethod
    def load(cls, path: Path) -> Rubik:
        coloring: ColoringCell = dict()
        with open(path, 'r') as f:
            for line in f:
                x, y, z, color = line.split()
                cell_a = Vector(int(x), int(y), int(z))
                cell_b = cell(color)
                coloring[cell_a] = cell_b
        cls.coloring = coloring
        return cls(coloring)

    def save(self, path: Path):
        # TODO
        pass



if __name__ == '__main__':

    R = Rubik()
    R.act(Color.R).act(Color.R).act(Color.R).act(Color.B).act(Color.R)
    R.apply("RRRBR")
    for c, v in R.coloring.items():
        if c == v:
            continue
        print(c, '->', v, '\t', R.cells_index[c], R.cells_index[v])

    from example_rubik_state import *
    coloring = {Vector(*v): cell(s) for v, s in state_230430_0946.items()}
    for a, b in coloring.items():
        print(a, b)
    R = Rubik(coloring)
    p = R.permutation()
    print(p)

    from permutation import RubikSmallGroup
    rsg = RubikSmallGroup()
