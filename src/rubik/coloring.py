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
