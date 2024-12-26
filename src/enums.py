from enum import Enum, auto


class State(Enum):
    GAME = auto()
    MENU = auto()
    SERVER_FINDER = auto()
    LOBBY = auto()
