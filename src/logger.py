import inspect
import time
from pathlib import Path

import colorama


def color_text(text: str, color: str) -> str:
    return getattr(colorama.Fore, color.upper()) + text + colorama.Fore.RESET


def log(*objects, color: str = "white") -> None:
    frame = inspect.currentframe()
    caller_frame = frame.f_back

    file_name = Path(caller_frame.f_code.co_filename).name
    line_number = caller_frame.f_lineno

    output = color_text("[LOG]", "green")
    output += color_text(f"[{time.time():.0f}]", "cyan")
    output += color_text(f"[{file_name}:{line_number}] ", "blue")
    output += color_text(" ".join(map(str, objects)), color)

    print(output)
