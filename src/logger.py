import inspect


def log(*objects) -> None:
    frame = inspect.currentframe()
    caller_frame = frame.f_back

    file_name = caller_frame.f_code.co_filename
    line_number = caller_frame.f_lineno

    print(f"[LOG][{file_name}:{line_number}] ", *objects)
