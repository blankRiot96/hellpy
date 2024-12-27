from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from src.enums import State

MENU_WIDTH = 1280
MENU_HEIGHT = 800

current_state: State
is_host = False
debug_mode: bool
client_name: str
