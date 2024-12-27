from raylib import *

from src import shared


class LobbyState:
    def __init__(self):
        if shared.is_host:
            self.create_server()
        self.create_client()

    def create_server(self):
        pass

    def create_client(self):
        pass

    def update(self):
        pass

    def draw(self):
        DrawFPS(10, 10)
        DrawText(b"LOBBY", 10, 30, 32, RED)
        DrawText(f"CLIENT: {shared.client_name}".encode(), 10, 60, 24, RED)
