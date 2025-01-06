import math

from pyray import *
from raylib.defines import KEY_DOWN

from src import shared
from src.asset_manager import ModelID
from src.logger import log
from src.packets import Packet

SPEED = 10


class Player:
    def __init__(self):
        self.pos = Vector3(0, 0, 0)
        # self.pos.x = get_random_value(0, shared.MENU_WIDTH)
        # self.pos.y = get_random_value(0, shared.MENU_HEIGHT)
        # self.pos.z = get_random_value(-100, 100)

        if shared.model_id_argc is None:
            self.model_id = ModelID.CUBE_MAN
        else:
            self.model_id = getattr(ModelID, shared.model_id_argc)
        t = lambda: get_random_value(100, 255)
        self.color = Color(t(), t(), t(), 255)
        self.angle = 0.0

    def compute_angle_from_cam_z(
        self, cam_z: float, offset: float, scale: float
    ) -> None:
        total = math.pi / 2
        ratio = cam_z / (offset * scale)
        self.angle = -total * ratio
        # Um dz or dx correction
        self.angle += math.pi / 2

    def update(self):
        # Get input for forward/backward (W/S) and strafing (A/D)
        forward = is_key_down(KeyboardKey.KEY_W) - is_key_down(KeyboardKey.KEY_S)
        strafe = is_key_down(KeyboardKey.KEY_A) - is_key_down(KeyboardKey.KEY_D)

        # Compute movement vector based on player's angle
        dx = math.sin(self.angle) * forward + math.cos(self.angle) * strafe
        dz = math.cos(self.angle) * forward - math.sin(self.angle) * strafe

        # Normalize movement vector to prevent diagonal speed boost
        magnitude = math.sqrt(dx**2 + dz**2)
        if magnitude > 0:
            dx /= magnitude
            dz /= magnitude

        # Update position
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
        model = shared.asset_manager.get_model_from_id(
            ModelID.from_value(packet.model_id)
        )

        # draw_cube(pos, 1, 1, 1, packet.color)
        # draw_cube_wires(pos, 1, 1, 1, WHITE)

        model.transform = matrix_rotate_y(packet.angle)
        draw_model(model, pos, 1, packet.color)
        draw_model_wires(model, pos, 1, WHITE)

    def draw_3d(self):
        self.draw_from_packet_3d(shared.client.create_packet())

    def draw(self):
        self.draw_from_packet(shared.client.create_packet())
