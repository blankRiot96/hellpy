import queue
import socket
import threading
import time
from queue import Empty, PriorityQueue, Queue

from src import shared
from src.logger import log

HOST, PORT = socket.gethostbyname(socket.gethostname()), shared.PORT


class Server:
    """
    - Receives client data {"pos": [x, y], "state": "..."}
    - Sends client data to all other clients
    """

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        shared.server_ip = HOST

    def process_server(self):
        self.socket.listen()
        log(f"Server started at {HOST}:{PORT}", color="red")

        clients: list[socket.socket] = []

        def recv_all(sock, length):
            data = b""
            while len(data) < length:
                more = sock.recv(length - len(data))
                if not more:
                    raise EOFError("Socket closed before receiving all data")
                data += more
            return data

        def handle_client(client_socket: socket.socket, client_address):
            log(f"New connection from: {client_address}", color="red")

            while True:
                time.sleep(0)
                message_size = int.from_bytes(
                    recv_all(client_socket, shared.MSG_SIZE_SIZE)
                )
                message = recv_all(client_socket, message_size)
                size = len(message)
                if not message:
                    break

                queue.put([size, message, client_socket])

            clients.remove(client_socket)
            client_socket.close()

        def separate_function():
            while True:
                try:
                    size, message, client_socket = queue.get(timeout=0.1)
                except Empty:
                    continue

                for client in clients:
                    if client == client_socket:
                        continue

                    client.send(size.to_bytes(shared.MSG_SIZE_SIZE) + message)

        queue = Queue()

        threading.Thread(target=separate_function, daemon=True).start()

        while True:
            time.sleep(0)
            client_socket, client_address = self.socket.accept()
            clients.append(client_socket)
            threading.Thread(
                target=handle_client, args=(client_socket, client_address), daemon=True
            ).start()

    def start(self):
        """Start a server in a thread"""

        threading.Thread(target=self.process_server, daemon=True).start()

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)

    print(host)
