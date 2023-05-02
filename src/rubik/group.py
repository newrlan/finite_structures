from __future__ import annotations
from typing import List, Optional, Any, Tuple, Type, TypeVar
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from rubik.permutation import Permutation, RubikSmallGroup
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

    def permutation(
        self,
        coloring: Optional[ColoringCell] = None,
        subgroup: Optional[str] = None
    ) -> Permutation:
        """ Map coloring to permutation. """

        if coloring is None:
            coloring = self.coloring

        candidates = coloring.keys()
        if subgroup == 'vertex':
            candidates = [c for c in candidates if c.rank() == 3]

        perm = dict()
        # for a, b in coloring.items():
        for a in candidates:
            b = coloring[a]
            if a == b:
                continue
            i = self.cells_index[a]
            j = self.cells_index[b]
            perm[j] = i

        return Permutation(perm)

    def act(self, color: Color):
        coloring = dict()
        for v, c in self.coloring.items():
            d = rotate(v, color)
            coloring[d] = c
        self.coloring = coloring
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

    # cube = Rubik.load(Path('../../test/state_300423.txt'))
    cube = Rubik.load(Path('state.txt'))
    # cube = cube.act(Color.O)

    p = cube.permutation(subgroup='vertex')
    print('permutation:\t', p)
    word = RubikSmallGroup().permutation2word(p)
    print('word:\t', word)

    # cube = cube.act(Color.B)

    # p = cube.permutation(subgroup='vertex')
    # print('permutation:\t', p)
    # word = RubikSmallGroup().permutation2word(p)
    # # word = 'OOOBOBBOOOBBBOBBBYYYBBYB' + 'OOOWOBBOOOWWWOBYOOYYYBBB'
    # print('word:\t', word)

    # q = RubikSmallGroup().word2permutation(word)
    # print("p * q =", p * q)

    cube.apply(word)
    for v, w in cube.coloring.items():
        if v == w or v.rank() != 3:
            continue
        print(v, w)

    for w in word:
        print(w)
        input("")
