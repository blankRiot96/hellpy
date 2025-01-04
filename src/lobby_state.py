from pyray import *
from raylib import CAMERA_FREE, CAMERA_PERSPECTIVE, CAMERA_THIRD_PERSON

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
        shared.camera.projection = CAMERA_PERSPECTIVE
        shared.camera.position = Vector3(10, 10, 10)  # Adjust based on your scene
        shared.camera.target = shared.player.pos
        shared.camera.up = Vector3(0, 1, 0)
        shared.camera.fovy = 45.0

    def update(self):
        shared.player.update()

    def draw(self):
        # update_camera(shared.camera, CAMERA_FREE)

        draw_fps(10, 10)
        draw_text("LOBBY", 10, 30, 32, RED)
        draw_text(f"CLIENT: {shared.client_name}", 10, 60, 24, RED)
        shared.player.draw()

        for packet in shared.client.other_client_packets.values():
            shared.player.draw_from_packet(packet)

        begin_mode_3d(shared.camera)

        shared.player.draw_3d()
        for packet in shared.client.other_client_packets.values():
            shared.player.draw_from_packet_3d(packet)

        # draw_cube(Vector3(0, 0, 0), 1, 1, 1, BLUE)  # Debug cube at origin
        end_mode_3d()
