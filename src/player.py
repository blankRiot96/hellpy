from dataclasses import dataclass

from raylib import *

from src import shared
from src.packets import Packet, Vector2


@dataclass
class Color:
    r: int = 0
    g: int = 0
    b: int = 0


SPEED = 100


class Player:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.pos.x = GetRandomValue(0, shared.MENU_WIDTH)
        self.pos.y = GetRandomValue(0, shared.MENU_HEIGHT)
        self.color = Color()
        self.color.r = GetRandomValue(100, 255)
        self.color.g = GetRandomValue(100, 255)
        self.color.b = GetRandomValue(100, 255)
        shared.client.packet.color = (self.color.r, self.color.b, self.color.g, 255)

    def update(self):
        dx = IsKeyDown(KEY_D) - IsKeyDown(KEY_A)
        dy = IsKeyDown(KEY_S) - IsKeyDown(KEY_W)

        self.pos.x += SPEED * dx * GetFrameTime()
        self.pos.y += SPEED * dy * GetFrameTime()

        shared.client.packet.pos = self.pos

    @staticmethod
    def draw_from_packet(packet: Packet) -> None:
        px, py = int(packet.pos.x), int(packet.pos.y)
        DrawRectangle(px, py, 50, 50, packet.color)
        DrawText(packet.name.encode(), px, py, 20, GREEN)

    def draw(self):
        self.draw_from_packet(shared.client.packet)
