import socket
import threading
import time

from src import shared
from src.logger import log
from src.packets import Packet


class Client:
    """
    - Sends data packet to server
    - Receives other client information and stores it
    """

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.other_client_packets: dict[str, Packet] = {}
        self.ready_to_send = True

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
                self.ready_to_send = True
                # log(self.other_client_packets, color="green")

        threading.Thread(target=receive_data, daemon=True).start()
        self.send_data()
        while True:
            # time.sleep(0)
            time.sleep(0.0001)  # ~0.1ms PING minimum

            self.send_data()

    def send_data(self):
        # if not self.ready_to_send or not hasattr(shared, "world"):
        if not hasattr(shared, "world"):
            return

        packet = self.create_packet()
        message = packet.to_json().encode()
        size = len(message)

        self.socket.send(size.to_bytes(shared.MSG_SIZE_SIZE) + message)
        self.ready_to_send = False

    def create_packet(self) -> Packet:
        pos = shared.world.player.pos
        color = shared.world.player.color
        return Packet(
            name=shared.client_name,
            pos=[pos.x, pos.y, pos.z],
            color=[color.r, color.g, color.b, color.a],
            model_id=shared.world.player.model_id.value,
            angle=shared.world.player.angle,
        )

    def start(self):
        """Starts a client in a thread"""

        threading.Thread(target=self.process_client, daemon=True).start()

    def close(self):
        self.socket.close()
