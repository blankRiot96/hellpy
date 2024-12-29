from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from src.client import Client
    from src.enums import State
    from src.packets import Packet
    from src.server import Server

MENU_WIDTH = 1920 // 2
MENU_HEIGHT = 1020
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
