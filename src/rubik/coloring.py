from __future__ import annotations
from typing import List, Optional, Any, Tuple, Type, TypeVar
from dataclasses import dataclass, field
from enum import Enum

from rubik.permutation import Permutation


class Vector:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, vector: Vector) -> Vector:
        return Vector(self.x + vector.x,
                      self.y + vector.y,
                      self.z + vector.z)

    def _rotate_x(self) -> Vector:
        e = 2 * (self.x > 0) - 1
        return Vector(self.x, e * self.z, - e * self.y)

    def _rotate_y(self) -> Vector:
        e = 2 * (self.y > 0) - 1
        return Vector(- e * self.z, self.y, e * self.x)

    def _rotate_z(self) -> Vector:
        e = 2 * (self.z > 0) - 1
        return Vector(e * self.y, - e * self.x, self.z)

    def rotate(self, axis: int) -> Vector:
        """ Развернуть вектор на 90 градусов вокруг оси axis по часовой стрелке."""
        if not axis < 3:
            raise ValueError("Vector can be rotated around axis 0, 1 or 2.")

        if axis == 0:
            return self._rotate_x()
        if axis == 1:
            return self._rotate_y()
        return self._rotate_z()

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def is_axis(self) -> bool:
        return abs(self.x) + abs(self.y) + abs(self.z) == 1

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, vector: Vector) -> bool:
        return (self.x == vector.x) & (self.y == vector.y) & (self.z == vector.z)

    def __repr__(self) -> str:
        return f"Vector {self.x} {self.y} {self.z}"

    def rank(self):
        return sum([x != 0 for x in self])


ColoringCell = dict[Vector, Vector]


class Color(Enum):
    B = Vector(1, 0, 0)
    Y = Vector(0, 1, 0)
    O = Vector(0, 0, 1)  # noqa: E741
    G = Vector(-1, 0, 0)
    W = Vector(0, -1, 0)
    R = Vector(0, 0, -1)


def rotate(vect: Vector, axis: Color) -> Vector:
    if sum([a * b for a, b in zip(axis.value, vect)]) != 1:
        return vect

    i = abs(1 * axis.value.y) + abs(2 * axis.value.z)
    e = sum(axis.value)
    x, y, z = vect
    if i == 0:
        return Vector(x, e * z, - e * y)
    if i == 1:
        return Vector(-e * z, y, e * x)
    return Vector(e * y, - e * x, z)


def cell(line: str) -> Vector:
    try:
        colors = [Color.__members__[w].value for w in line]
    except KeyError:
        raise ValueError(f"Line {line} has unknown color.")
    ans = colors[0]
    for v in colors[1:]:
        ans += v
    return ans


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
            perm[i] = j

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
