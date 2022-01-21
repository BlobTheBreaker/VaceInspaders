import socket

HOST = socket.gethostbyname(socket.gethostname()) # Default: Server and client on the same computer
PORT = 5555

class Network():
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.adress = host, port

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.adress)
        data = self.sock.recv(2048).decode('UTF-8')
        print(data)

    def send(self, msg):
        self.sock.send(str(msg).encode())
        data = self.sock.recv(2048).decode('UTF-8')
        return data
