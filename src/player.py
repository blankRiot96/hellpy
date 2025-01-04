from pyray import *

from src import shared
from src.logger import log
from src.packets import Packet

SPEED = 300


class Player:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.pos.x = get_random_value(0, shared.MENU_WIDTH)
        self.pos.y = get_random_value(0, shared.MENU_HEIGHT)

        t = lambda: get_random_value(100, 255)
        self.color = Color(t(), t(), t(), 255)

    def update(self):
        dx = is_key_down(KeyboardKey.KEY_D) - is_key_down(KeyboardKey.KEY_A)
        dy = is_key_down(KeyboardKey.KEY_A) - is_key_down(KeyboardKey.KEY_W)

        self.pos.x += SPEED * dx * get_frame_time()
        self.pos.y += SPEED * dy * get_frame_time()

    @staticmethod
    def draw_from_packet(packet: Packet) -> None:
        px, py = int(packet.pos[0]), int(packet.pos[1])
        draw_rectangle(px, py, 50, 50, packet.color)
        draw_text(packet.name, px, py - 20, 20, GREEN)

    def draw(self):
        self.draw_from_packet(shared.client.create_packet())
