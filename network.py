import socket

HOST = socket.gethostbyname(socket.gethostname()) # Default: Server and client on the same computer
PORT = 5555

class Network():
    def __init__(self, host=HOST, port=PORT): # Pretty straight forward
        self.host = host
        self.port = port
        self.adress = host, port

    def connect(self): # Handles the connection to the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.adress)
        data = self.sock.recv(2048).decode('UTF-8') # Receives the client token
        print(data) # Only prints it for now

    def send(self, msg): # Sends to the server
        self.sock.send(str(msg).encode()) # Any type that can make a str, gets encoded and sent
        data = self.sock.recv(2048).decode('UTF-8')  # Gets the server's response, decodes it
        return data # and returns it
