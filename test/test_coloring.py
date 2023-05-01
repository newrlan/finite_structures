from rubik.coloring import Vector
import pytest


def test_Vector_add():
    v1 = Vector(1, 2, 4)
    v2 = Vector(-1, -2, -4)

    v3 = v1 + v2
    assert v3.x == 0
    assert v3.y == 0
    assert v3.z == 0


vectors_rotation_set = [
    # -- z
    (Vector(1, 0, 3), 2, Vector(0, -1, 3)),
    (Vector(0, 1, 3), 2, Vector(1, 0, 3)),
    (Vector(1, 0, -3), 2, Vector(0, 1, -3)),
    (Vector(0, 1, -3), 2, Vector(-1, 0, -3)),
    # -- y
    (Vector(1, 3, 0), 1, Vector(0, 3, 1)),
    (Vector(0, 3, 1), 1, Vector(-1, 3, 0)),
    (Vector(1, -3, 0), 1, Vector(0, -3, -1)),
    (Vector(0, -3, 1), 1, Vector(1, -3, 0)),
    # -- x
    (Vector(3, 1, 0), 0, Vector(3, 0, -1)),
    (Vector(3, 0, 1), 0, Vector(3, 1, 0)),
    (Vector(-3, 1, 0), 0, Vector(-3, 0, 1)),
    (Vector(-3, 0, 1), 0, Vector(-3, -1, 0)),
]


@pytest.mark.parametrize('vector, axis, answer', vectors_rotation_set)
def test_Vector_rotate(vector, axis, answer):
    w = vector.rotate(axis)
    assert w == answer
