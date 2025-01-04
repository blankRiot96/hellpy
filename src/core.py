import argparse
import sys

from pyray import *

from src import shared
from src.enums import State
from src.logger import log
from src.states import StateObj


class Core:
    def __init__(self):
        set_trace_log_level(TraceLogLevel.LOG_ERROR)
        self.process_cli()

        set_config_flags(ConfigFlags.FLAG_WINDOW_RESIZABLE)
        init_window(shared.MENU_WIDTH, shared.MENU_HEIGHT, "Hell")
        set_window_position(2 + int(shared.MENU_WIDTH * shared.window_open_flag), 50)
        shared.current_state = State.MENU
        self.state_obj = StateObj()

    def process_cli(self):
        log(sys.argv)
        self.parser = argparse.ArgumentParser(prog="HELL")
        self.parser.add_argument(
            "-d", "--debug", action="store_true", help="Debug mode"
        )
        self.parser.add_argument("-w", "--window", default=0, help="Window open mode")
        self.parser.add_argument("--ip", help="Host's IP")

        args = self.parser.parse_args()
        if args.debug is True:
            shared.debug_mode = True

        shared.window_open_flag = int(args.window)
        if args.ip:
            shared.server_ip = args.ip

        log(f"{shared.server_ip = }", color="green")

    def update(self):
        self.state_obj.update()

    def draw(self):
        begin_drawing()
        clear_background(BLACK)
        self.state_obj.draw()
        end_drawing()

    def cleanup(self):
        if hasattr(shared, "server"):
            shared.server.close()
        if hasattr(shared, "client"):
            shared.client.close()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()

        self.cleanup()


def main():
    core = Core()
    core.run()
