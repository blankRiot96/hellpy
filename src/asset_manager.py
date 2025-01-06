from enum import Enum, auto
from functools import lru_cache

import pyray


class ModelID(Enum):
    CUBE_MAN = auto()
    TANKY_BOI = auto()

    @lru_cache
    @staticmethod
    def from_value(value: int):
        return {id.value: id for id in ModelID}[value]


MODEL_MAP: dict[ModelID, str] = {
    ModelID.CUBE_MAN: "assets/cube.obj",
    ModelID.TANKY_BOI: "assets/tanky.obj",
}


class AssetManager:
    def __init__(self) -> None:
        self.models: dict[ModelID, pyray.Model] = {}

    def get_model_from_id(self, model_id: ModelID) -> pyray.Model:
        if model_id not in self.models:
            self.models[model_id] = pyray.load_model(MODEL_MAP[model_id])

        return self.models[model_id]
