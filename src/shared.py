from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from src.client import Client
    from src.enums import State
    from src.packets import Packet
    from src.server import Server

MENU_WIDTH = 1280
MENU_HEIGHT = 800
PORT = 3005
MSG_SIZE_SIZE = 4

current_state: State
is_host = False
debug_mode: bool
client_name: str
server_ip: str

server: Server
client: Client
