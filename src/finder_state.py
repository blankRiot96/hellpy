from pyray import *
from raylib import DEFAULT, TEXT_SIZE

from src import shared
from src.enums import State


class FinderState:
    def __init__(self):
        gui_set_style(DEFAULT, TEXT_SIZE, 32)
        self.server_code = ""

    def update(self):
        pass

    def draw(self):
        gui_text_box((10, 10, 200, 70), self.server_code, 32, True)

        if gui_button((10, 90, 200, 70), "FIND"):
            shared.current_state = State.LOBBY
