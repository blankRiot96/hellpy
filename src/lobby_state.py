from pyray import *

from src import shared
from src.client import Client
from src.logger import log
from src.server import Server
from src.world import World


class LobbyState:
    def __init__(self):
        if shared.is_host:
            shared.server = Server()
            shared.server.start()
        shared.client = Client()
        shared.client.start()

        shared.world = World()
        # disable_cursor()

    def update(self):
        shared.world.update()

    def draw(self):
        draw_fps(10, 10)
        draw_text("LOBBY", 10, 30, 32, RED)
        draw_text(f"CLIENT: {shared.client_name}", 10, 60, 24, RED)

        shared.world.draw()
