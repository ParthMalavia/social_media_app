import socket
import threading

MSG_SIZE = 2048
PORT = 5050
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER_IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "/disconnect"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)

while True:
    msg = input("Write message:")
    client.send(msg.encode(FORMAT))
    if msg == DISCONNECT_MSG:
        break
