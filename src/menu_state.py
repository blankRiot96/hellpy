import random

from raylib import *

from src import shared
from src.enums import State

BUTTON_WIDTH = 300
BUTTON_HEIGHT = 100


class MenuState:
    def __init__(self):
        GuiSetStyle(DEFAULT, TEXT_SIZE, 32)

        self.client_name = f"guest{random.randint(1, 99)}".encode()

    def update(self):
        pass

    def draw(self):
        DrawText(b"Hell", int(shared.MENU_WIDTH / 2) - 55, 100, 45, RED)

        GuiTextBox(
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

        if GuiButton(
            (
                int(shared.MENU_WIDTH / 2) - int(BUTTON_WIDTH / 2),
                int(shared.MENU_HEIGHT / 2) - int(BUTTON_HEIGHT / 2),
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
            b"FIND SERVER",
        ):
            shared.client_name = self.client_name.decode()
            shared.current_state = State.SERVER_FINDER

        if GuiButton(
            (
                int(shared.MENU_WIDTH / 2) - int(BUTTON_WIDTH / 2),
                int(shared.MENU_HEIGHT / 2) + int(BUTTON_HEIGHT / 2) + 20,
                BUTTON_WIDTH,
                BUTTON_HEIGHT,
            ),
            b"CREATE SERVER",
        ):
            shared.client_name = self.client_name.decode()
            shared.is_host = True
            shared.current_state = State.LOBBY
