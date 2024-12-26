from raylib import *

from src import shared
from src.enums import State
from src.states import StateObj


class Core:
    def __init__(self):
        InitWindow(shared.MENU_WIDTH, shared.MENU_HEIGHT, b"Hell")
        shared.current_state = State.MENU
        self.state_obj = StateObj()

    def update(self):
        self.state_obj.update()

    def draw(self):
        BeginDrawing()
        ClearBackground(BLACK)
        self.state_obj.draw()
        EndDrawing()

    def run(self):
        while not WindowShouldClose():
            self.update()
            self.draw()


def main():
    core = Core()
    core.run()
