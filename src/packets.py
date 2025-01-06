import json
import typing as t
from dataclasses import asdict, dataclass


@dataclass
class Packet:
    """Information about client's state to send over the network"""

    name: str
    pos: list[float]
    color: list[int]
    model_id: int
    angle: float

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, json_data: str) -> t.Self:
        return cls(**json.loads(json_data))
