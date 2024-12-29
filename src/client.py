import socket
import threading
import time

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
        self.packet = Packet(Vector2(0, 0), shared.client_name, (255, 255, 255, 255))

    def process_client(self):
        HOST, PORT = shared.server_ip, shared.PORT
        self.socket.connect((HOST, PORT))
        log(f"Connected to {HOST}:{PORT}", color="magenta")

        def recv_all(sock, length):
            data = b""
            while len(data) < length:
                more = sock.recv(length - len(data))
                if not more:
                    raise EOFError("Socket closed before receiving all data")
                data += more
            return data

        def receive_data():
            while True:
                time.sleep(0)
                message_size = int.from_bytes(
                    recv_all(self.socket, shared.MSG_SIZE_SIZE)
                )
                message = recv_all(self.socket, message_size)
                if not message:
                    break

                packet = Packet.from_json(message.decode())
                self.other_client_packets[packet.name] = packet
                # log(self.other_client_packets, color="green")

        threading.Thread(target=receive_data, daemon=True).start()
        while True:
            time.sleep(0)
            message = self.packet.to_json().encode()
            size = len(message)

            self.socket.send(size.to_bytes(shared.MSG_SIZE_SIZE) + message)

    def start(self):
        """Starts a client in a thread"""

        threading.Thread(target=self.process_client, daemon=True).start()

    def close(self):
        self.socket.close()
