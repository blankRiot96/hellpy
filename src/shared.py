from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from pyray import Camera3D

    from src.client import Client
    from src.enums import State
    from src.player import Player
    from src.server import Server

MENU_WIDTH = 1280
MENU_HEIGHT = 720
PORT = 3005
MSG_SIZE_SIZE = 4


current_state: State
is_host = False
debug_mode: bool = False
window_open_flag: int = 0
client_name: str
server_ip: str | None = None

server: Server
client: Client
player: Player
camera: Camera3D
