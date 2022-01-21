import socket
from _thread import *
import socketserver


hostname = socket.gethostname()
HOST = socket.gethostbyname(hostname)
PORT  = 5555
ADRESS = HOST, PORT


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.bind(ADRESS)
    print('Server started, waiting for connection')
except:
    raise

def threaded_client(conn, client_id):  # This enables multiple clients to be handled at once
    
    conn.send('Hello Client {0}'.format(client_id).encode())
    while True:
            data = conn.recv(2048).decode('UTF-8')
            if data == 'exit':
                print('Client disconnected')
                conn.close()
                break

            else:
                print(data)
                reply = 'Message received: {}'.format(data)
                conn.sendall(reply.encode())


sock.listen(2)
client_id = 1

while True:
    conn, addr = sock.accept()

    print('Connected by {0}:{1}'.format(addr[0], addr[1]))
    start_new_thread(threaded_client, (conn, client_id))
    client_id += 1
