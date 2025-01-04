from pyray import *

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

        shared.player = Player()

    def update(self):
        shared.player.update()

    def draw(self):
        draw_fps(10, 10)
        draw_text("LOBBY", 10, 30, 32, RED)
        draw_text(f"CLIENT: {shared.client_name}", 10, 60, 24, RED)
        shared.player.draw()

        for packet in shared.client.other_client_packets.values():
            shared.player.draw_from_packet(packet)
