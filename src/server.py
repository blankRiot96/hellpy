import socket
import threading

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
        log(f"Server started at {HOST}:{PORT}")

        clients = []

        def handle_client(client_socket: socket.socket, client_address):
            log({f"New connection from: {client_address}"})

            while True:
                data = client_socket.recv(1024)
                if not data:
                    break

                for client in clients:
                    if client == client_socket:
                        continue

                    client.sendall(data)

            clients.remove(client_socket)
            client_socket.close()

        while True:
            client_socket, client_address = self.socket.accept()
            clients.append(client_socket)
            threading.Thread(
                target=handle_client, args=(client_socket, client_address)
            ).start()

    def start(self):
        """Start a server in a thread"""

        threading.Thread(target=self.process_server).start()

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    host_name = socket.gethostname()
    host = socket.gethostbyname(host_name)

    print(host)
