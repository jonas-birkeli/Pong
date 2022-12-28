import socket
import threading


class Client(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port

        self.client_socket = None

    def connect(self):
        self.client_socket = socket.socket()  # instantiate
        try:
            self.client_socket.connect((self.host, self.port))  # connect to the server
        except socket.error:
            print("Could not connect to host.")
            return -1
        return 0

    def send(self, item):
        self.client_socket.send(item.encode())

    def receive(self):
        data = self.client_socket.recv(1024).decode()
        if data.lower().strip() != 'end':
            return data
        self.client_socket.close()
        return 0
