from pyray import *

from src import shared, utils
from src.asset_manager import ModelID


class Decoration:
    """Just an idle decoration for the player to do stuff on"""

    def __init__(
        self, model_id: ModelID, pos: Vector3, tint=WHITE, draw_wires: bool = False
    ) -> None:
        self.model = shared.asset_manager.get_model_from_id(model_id)
        self.box = get_model_bounding_box(self.model)
        self.pos = pos

        utils.set_box_pos(self.box, self.pos)

        self.tint = tint
        self.draw_wires = draw_wires

    def update(self):
        pass

    def draw_3d(self):
        draw_model(self.model, self.pos, 1, self.tint)
        if self.draw_wires:
            draw_model_wires(self.model, self.pos, 1, WHITE)


class DecorationManager:
    """Handles updating and rendering of decorative objects"""

    def __init__(self) -> None:
        self.decorations: list[Decoration] = []

    def update(self):
        for decoration in self.decorations:
            decoration.update()

    def draw_3d(self):
        for decoration in self.decorations:
            decoration.draw_3d()
