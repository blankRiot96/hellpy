import random

from pyray import *
from raylib import DEFAULT, TEXT_SIZE

from src import shared
from src.enums import State

BUTTON_WIDTH = 300
BUTTON_HEIGHT = 100


class MenuState:
    def __init__(self):
        gui_set_style(DEFAULT, TEXT_SIZE, 32)
        self.client_name = f"guest{random.randint(1, 99)}"

    def update(self):
        pass

    def draw(self):
        draw_text("Hell", int(shared.MENU_WIDTH / 2) - 55, 100, 45, RED)

        gui_text_box(
            (
                int(shared.MENU_WIDTH / 2) - int(BUTTON_WIDTH / 2),
                int(shared.MENU_HEIGHT / 2) - BUTTON_HEIGHT - 100,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
            self.client_name,
            32,
            True,
        )

        if gui_button(
            (
                int(shared.MENU_WIDTH / 2) - int(BUTTON_WIDTH / 2),
                int(shared.MENU_HEIGHT / 2) - int(BUTTON_HEIGHT / 2),
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
            "FIND SERVER",
        ):
            shared.client_name = self.client_name
            shared.current_state = State.SERVER_FINDER

        if gui_button(
            (
                int(shared.MENU_WIDTH / 2) - int(BUTTON_WIDTH / 2),
                int(shared.MENU_HEIGHT / 2) + int(BUTTON_HEIGHT / 2) + 20,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
            "CREATE SERVER",
        ):
            shared.client_name = self.client_name
            shared.is_host = True
            shared.current_state = State.LOBBY
