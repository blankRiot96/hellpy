from pyray import *

from src import shared
from src.logger import log
from src.packets import Packet

SPEED = 10


class Player:
    def __init__(self):
        self.pos = Vector3(0, 0, 0)
        # self.pos.x = get_random_value(0, shared.MENU_WIDTH)
        # self.pos.y = get_random_value(0, shared.MENU_HEIGHT)
        # self.pos.z = get_random_value(-100, 100)

        t = lambda: get_random_value(100, 255)
        self.color = Color(t(), t(), t(), 255)

    def update(self):
        dx = is_key_down(KeyboardKey.KEY_D) - is_key_down(KeyboardKey.KEY_A)
        dz = is_key_down(KeyboardKey.KEY_S) - is_key_down(KeyboardKey.KEY_W)

        self.pos.x += SPEED * dx * get_frame_time()
        self.pos.z += SPEED * dz * get_frame_time()

    @staticmethod
    def draw_from_packet(packet: Packet) -> None:
        # px, py = int(packet.pos[0]), int(packet.pos[1])
        # draw_rectangle(px, py, 50, 50, packet.color)
        # draw_text(packet.name, px, py - 20, 20, GREEN)
        pass

    @staticmethod
    def draw_from_packet_3d(packet: Packet) -> None:
        pos = Vector3(*packet.pos)
        draw_cube(pos, 1, 1, 1, packet.color)
        draw_cube_wires(pos, 1, 1, 1, WHITE)

    def draw_3d(self):
        self.draw_from_packet_3d(shared.client.create_packet())

    def draw(self):
        self.draw_from_packet(shared.client.create_packet())
