import math

from pyray import *

from src import shared
from src.asset_manager import ModelID
from src.decorations import Decoration, DecorationManager
from src.logger import log
from src.player import Player


class World:
    """Handle updating, rendering and some interaction between world objects"""

    def __init__(self) -> None:
        self.player = Player()

        shared.camera = Camera3D()
        shared.camera.projection = CameraProjection.CAMERA_PERSPECTIVE
        shared.camera.position = Vector3(10, 10, 10)
        shared.camera.target = self.player.pos
        shared.camera.up = Vector3(0, 1, 0)
        shared.camera.fovy = 30.0

        self.dec_manager = DecorationManager()

        root_dec = Decoration(ModelID.FLOOR, Vector3(0, -1, 0), GREEN, draw_wires=True)
        self.dec_manager.decorations.append(root_dec)

        size = root_dec.box.max.z - root_dec.box.min.z
        for i in range(0, 5):
            self.dec_manager.decorations.append(
                Decoration(
                    ModelID.FLOOR,
                    Vector3(0, i, size * (i + 1)),
                    color_lerp(GREEN, PURPLE, i * 0.3),
                    draw_wires=True,
                )
            )

        self.prev_mouse_pos = get_mouse_position()
        self.cam_y = 0.0

    def adjust_camera_position(self):
        mouse_pos = get_mouse_position()
        y_delta = mouse_pos.y - self.prev_mouse_pos.y
        self.prev_mouse_pos.x, self.prev_mouse_pos.y = mouse_pos.x, mouse_pos.y

        y_rotat_scale = 0.0025
        self.cam_y += y_delta * y_rotat_scale
        self.cam_y = clamp(self.cam_y, -1.75, 1.75)

        distance = 10  # Distance behind the player
        height = 2 + self.cam_y  # Camera height relative to the player
        cam_dx = math.sin(self.player.angle) * distance
        cam_dz = math.cos(self.player.angle) * distance

        shared.camera.position = vector3_add(
            self.player.pos, (-cam_dx, height, -cam_dz)
        )
        shared.camera.target = self.player.pos

    def update(self):
        self.player.compute_angle()
        self.adjust_camera_position()

        self.player.update()
        self.dec_manager.update()

    def draw(self):
        begin_mode_3d(shared.camera)

        # Ground
        self.dec_manager.draw_3d()

        # Players
        self.player.draw_3d()
        # print(shared.client.other_client_packets)
        for packet in shared.client.other_client_packets.values():
            self.player.draw_from_packet_3d(packet)

        end_mode_3d()
