from pyray import *


def set_box_pos(box: BoundingBox, pos: Vector3, scale: float = 1.0) -> None:
    # box.min = vector3_scale(box.min, scale)
    # box.max = vector3_scale(box.max, scale)

    box.min = vector3_add(box.min, pos)
    box.max = vector3_add(box.max, pos)
