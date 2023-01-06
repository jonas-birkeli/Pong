import socket
import threading
import select


class Client(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.client_socket = socket.socket()
        self.client_socket.setblocking(False)
        self.id = None
        self.game_started = False

    def connect(self):
        """Connect to the server."""
        try:
            self.client_socket.connect((self.host, self.port))
            return 1
        except:
            return -1

    def disconnect(self):
        """Disconnect from the server."""
        self.client_socket.close()

    def receive_data(self):
        """Receive data from the server and process it."""
        try:
            data = self.client_socket.recv(1024).decode()
            if data:
                self.process_data(data)
        except:
            pass

    def process_data(self, data):
        if data.startswith("ID"):
            if data[-1] == 'T':  # 'START' from server
                self.id = 1
            else:
                self.id = int(data.split()[1])
        elif data == "START":
            # The game has started, so set the game_started flag to True
            self.game_started = True

    def send_data(self, data):
        """Send data to the server."""
        self.client_socket.send(data.encode())


