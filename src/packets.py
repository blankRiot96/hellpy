import json
import typing as t
from dataclasses import dataclass

from raylib import *

from src.logger import log


@dataclass
class Vector2:
    x: int = 0
    y: int = 0


@dataclass
class Packet:
    pos: Vector2
    name: str
    color: tuple

    def to_json(self) -> str:
        d = {"pos": [self.pos.x, self.pos.y], "name": self.name, "color": self.color}

        return json.dumps(d)

    @classmethod
    def from_json(cls, json_data: str) -> t.Self:
        try:
            d = json.loads(json_data)
        except Exception as e:
            log(json_data, color="cyan")
            raise e

        pos = Vector2()
        pos.x, pos.y = d["pos"]
        return cls(pos=pos, name=d["name"], color=d["color"])
