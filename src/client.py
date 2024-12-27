import socket
import threading

from raylib import *

from src import shared
from src.logger import log
from src.packets import Packet, Vector2


class Client:
    """
    - Sends data packet to server
    - Receives other client information and stores it
    """

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.other_client_packets: dict[str, Packet] = {}
        self.packet = Packet(Vector2(0, 0), shared.client_name)

    def process_client(self):
        HOST, PORT = shared.server_ip, shared.PORT
        self.socket.connect((HOST, PORT))
        log(f"Connected to {HOST}:{PORT}")

        def receive_data():
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break

                packet = Packet.from_json(data.decode())
                self.other_client_packets[packet.name] = packet

        threading.Thread(target=receive_data, daemon=True).start()
        while True:
            self.socket.send(self.packet.to_json().encode())

    def start(self):
        """Starts a client in a thread"""

        threading.Thread(target=self.process_client).start()

    def close(self):
        self.socket.close()
