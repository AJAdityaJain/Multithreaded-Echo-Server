import time
import threading
import socket

HOST, PORT = "localhost", 8080

class Task:
    def __init__(self, fn, args):
        self.func = fn
        self.args = args

class ThreadWorker:
    def __init__(self, n):
        self.n = n
        self.thread = threading.Thread(target=self.work,args=())
        self.task = None

    def work(self):
        print('Started worker')
        while True:
            if self.task != None:
                #If assigned then do task
                self.task.func(self.task.args)
                self.task = None

class ThreadQueuer:
    def __init__(self, workers):
        self.queueMutex = threading.Lock()
        self.queue = []

        self.idle = [ThreadWorker(i) for i in range(workers)]
        self.busy = []

    def start(self):
        print('Started boss')
        for worker in self.idle:
            worker.thread.start()
        while True:
            if len(self.queue) != 0 and len(self.idle) != 0:
                #Idle worker + Pending Task = Assigning said task to said worker
                worker = self.idle.pop()
                self.queueMutex.acquire()
                worker.task = self.queue.pop()
                self.queueMutex.release()
                self.busy.append(worker)
                
            #If workers was in busy[] but has no task ie worker completed task so assign new task
            for worker in self.busy:
                if worker.task == None:
                    self.idle.append(worker)
                    self.busy.remove(worker)


class SocketServer:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen(5)
        self.socket.settimeout(5)
        self.alive = True

    def handle_client(self, client_socket):
        data = client_socket.recv(1024).decode('utf-8')

        if data.strip().lower() == 'ping':
            time.sleep(2) # Time taken for dramatic purposes
            print("Ponged a ping")
            client_socket.send(b'pong')
        client_socket.close()

    def start(self):
        print(f"Server started at {HOST}:{PORT}")
        while self.alive:
            try:
                client_socket, addr = self.socket.accept()
                #On recieving a client assign it a task/position on a queuee
                queue.queueMutex.acquire()
                queue.queue.append(Task(self.handle_client,client_socket))
                queue.queueMutex.release()
            except socket.timeout:
                pass

if __name__ == "__main__":
    #Main thread redirects requests to the Boss thread
    #Boss thread Maintains worker threads and their tasks
    #Worker threads do actual task
    queue = ThreadQueuer(workers=10)
    boss_thread = threading.Thread(target=queue.start)
    boss_thread.start()
    
    server = SocketServer()
    server.start()