import time
import signal
import socket
from concurrent.futures import ThreadPoolExecutor

HOST, PORT = "localhost", 8080
class SocketServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        self.socket.settimeout(5)
        self.alive = True
        print(f"Server started at {HOST}:{PORT}")

    def die(self,signum,frame):
        print("Killed process")
        self.alive = False

    def handle_client(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            if data.strip().lower() == 'ping':
                time.sleep(2) # Time taken for dramatic purposes
                print("Ponged a ping")

            client_socket.send(b'pong')
        client_socket.close()

    def start(self):
        while self.alive:
            try:
                client_socket, addr = self.socket.accept()
                print(f"Connection from {addr} has been established.")
                executor.submit(self.handle_client, client_socket)            
            except socket.timeout:
                pass

if __name__ == "__main__":
    executor = ThreadPoolExecutor(max_workers=10)
    server = SocketServer()
    signal.signal(signal.SIGINT, server.die)
    signal.signal(signal.SIGTERM, server.die)

    server.start()
