import math

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
        shared.camera = Camera3D()
        shared.camera.projection = CameraProjection.CAMERA_PERSPECTIVE
        shared.camera.position = Vector3(10, 10, 10)  # Adjust based on your scene
        shared.camera.target = shared.player.pos
        shared.camera.up = Vector3(0, 1, 0)
        shared.camera.fovy = 30.0

        self.prev_mouse_pos = get_mouse_position()

    def update(self):
        shared.player.update()

    def draw(self):
        offset = shared.MENU_WIDTH / 2
        scale = 1 / 50
        cam_z = (get_mouse_position().x - offset) * scale
        cam_y = (get_mouse_position().y - (shared.MENU_HEIGHT / 2)) / 200

        shared.player.compute_angle_from_cam_z(cam_z, offset, scale)

        # Calculate camera position based on player's angle
        distance = 10  # Distance behind the player
        height = 2 + cam_y  # Camera height relative to the player
        cam_dx = math.sin(shared.player.angle) * distance
        cam_dz = math.cos(shared.player.angle) * distance

        # Set the camera's position and target
        shared.camera.position = vector3_add(
            shared.player.pos, (-cam_dx, height, -cam_dz)
        )
        shared.camera.target = shared.player.pos

        # update_camera(shared.camera, CameraMode.CAMERA_FREE)

        draw_fps(10, 10)
        draw_text("LOBBY", 10, 30, 32, RED)
        draw_text(f"CLIENT: {shared.client_name}", 10, 60, 24, RED)
        shared.player.draw()

        for packet in shared.client.other_client_packets.values():
            shared.player.draw_from_packet(packet)

        begin_mode_3d(shared.camera)

        draw_cube((0, -1, 0), 15, 1, 15, GREEN)
        draw_cube_wires((0, -1, 0), 15, 1, 15, WHITE)
        shared.player.draw_3d()
        for packet in shared.client.other_client_packets.values():
            shared.player.draw_from_packet_3d(packet)

        # draw_cube(Vector3(0, 0, 0), 1, 1, 1, BLUE)  # Debug cube at origin
        end_mode_3d()
