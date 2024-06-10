import socket
import sys
from threading import Thread
#Pass arg to client to send it to server
#Or use 'echo ping | ncat localhost 8080'

HOST, PORT = "localhost", 8080
data =  "ping"          #.join(sys.argv[1:])

def rapidfire(n):
    for _ in range(n):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            sock.sendall(bytes(data + "\n", "utf-8"))
            # received = str(sock.recv(1024), "utf-8")

t1 = Thread(target=rapidfire, args=(30,))
t2 = Thread(target=rapidfire, args=(40,))
t3 = Thread(target=rapidfire, args=(30,))

t1.start()
t1.join()
t2.start()
t2.join()
t3.start()
t3.join()