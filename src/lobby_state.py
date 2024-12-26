from raylib import *


class LobbyState:
    def __init__(self):
        pass

    def create_server(self):
        pass

    def create_client(self):
        pass

    def update(self):
        pass

    def draw(self):
        DrawFPS(10, 10)
        DrawText(f"LOBBY: {}", 10, 30, 32, RED)
