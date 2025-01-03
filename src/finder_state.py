from raylib import *

from src import shared
from src.enums import State


class FinderState:
    def __init__(self):
        GuiSetStyle(DEFAULT, TEXT_SIZE, 32)
        self.server_code = b""

    def update(self):
        pass

    def draw(self):
        GuiTextBox((10, 10, 200, 70), self.server_code, 32, True)

        if GuiButton((10, 90, 200, 70), b"FIND"):
            shared.current_state = State.LOBBY
