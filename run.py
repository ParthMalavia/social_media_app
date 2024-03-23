import socket
import threading

MSG_SIZE = 2048
PORT = 5050
SERVER_IP = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER_IP, PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "/disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def handle_client(conn: socket.socket, add):
    print(f"[New Connection {add}]")
    connected = True
    while connected:
        msg = conn.recv(MSG_SIZE).decode(FORMAT)
        print(len(msg))
        if msg:
            print(f"From [{add}]: {msg}")
            if msg == DISCONNECT_MSG:
                connected=False
        print(">>>")
    print("Current connections", threading.active_count())
    conn.close()

def start():
    print(f"Started listening to {ADDRESS} port")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("Current connections", threading.active_count())

start()

