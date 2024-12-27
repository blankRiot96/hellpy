from raylib import *

from src import shared
from src.client import Client
from src.player import Player
from src.server import Server


class LobbyState:
    def __init__(self):
        if shared.is_host:
            shared.server = Server()
            shared.server.start()
        shared.client = Client()
        shared.client.start()

        self.player = Player()

    def update(self):
        self.player.update()

    def draw(self):
        DrawFPS(10, 10)
        DrawText(b"LOBBY", 10, 30, 32, RED)
        DrawText(f"CLIENT: {shared.client_name}".encode(), 10, 60, 24, RED)
        self.player.draw()

        for packet in shared.client.other_client_packets:
            self.player.draw_from_packet(packet)
