from typing import List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum, auto, unique


@dataclass
class Axis:
    color: str
    axis: Vector
    action_s: List[int]
    action_b: List[int]


O = Axis('O', Vector(1, 0, 0), [1, 2, 3, 4], [9, 10])  # noqa: E741


@dataclass
class Vector:
    x: int
    y: int
    z: int

    def __add__(self, color):
        return Color(self.x + color.x, self.y + color.y, self.z + color.z)


class Axis(Enum):

    # TODO: check vectors

    O = Color(0, 0, 1)  # noqa: E741
    B = Color(1, 0, 0)
    Y = Color(0, 1, 0)

    R = Color(0, 0, -1)
    W = Color(-1, 0, 0)
    G = Color(0, -1, 0)



class Square:
    def __init__(self, coloring: List[str]):
        self.coloring = coloring

    @property
    def coloring(self) -> List[List[Axis]]:
        return self._coloring

    @coloring.setter
    def coloring(self, coloring: List[str]):
        if len(coloring) != 3 or any([len(arr) != 3 for arr in coloring]):
            raise ValueError("The coloring can't be set for square.")

        res = []
        for line in coloring:
            vector = []
            for w in line:
                if w not in Axis.__members__:
                    raise ValueError(f"Coloring has unknown color {w}.")
                vector.append()





        pass

@dataclass
class SquareColor:
    pic: List[str]
    _pic: List[str] = field(init=False, repr=False)

    @property
    def pic(self):
        return self._pic

    @pic.setter
    def pic(self, pic: List[str]):
        if len(pic) != 3:
            raise ValueError("The coloring can't be set for square.")
        for line in pic:
            if len(line) != 3:
                raise ValueError("The coloring can't be set for square.")
            for w in line:
                print(Axis.__members__)
                print(w, w in Axis.__members__)
                if w not in Axis.__members__:
                    raise ValueError("The coloring can't be set for square.")
        self._pic = pic

    def vectorize(self):
        center = self.pic[1][1]




class RubikCube:
    def __init__(self, coloring: List[SquareColor]):
        self.coloring = coloring

    def vectorize(self):
        pass
        
