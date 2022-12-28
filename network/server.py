import socket
import threading


class Server(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port

        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

        self.conn, self.addr = self.socket.accept()
        print(f'Connection from: {self.addr}')

    def send(self, item):
        self.conn.send(item.encode())

    def receive(self):
        data = self.conn.recv(1024).decode()
        if data.lower().strip() != 'end':
            return data
        self.conn.close()
        return 0
