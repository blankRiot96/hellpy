import socket

with open("test_ip.txt", "w") as f:
    ip = socket.gethostbyname(socket.gethostname())
    f.write(ip)
