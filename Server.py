import socket
from _thread import *
import socketserver


hostname = socket.gethostname() # Gets the local name of the computer running the server
HOST = socket.gethostbyname(hostname) # Translates the name into it's IP adress
PORT  = 5555 # Generally unused port (use netstat - aon to view used ports in cmd)
ADRESS = HOST, PORT

"""
Variable 'sock' holds an instance of the class socket (from the module socket) that is configured
for connection of type AF_INET = IPv4 of protocol SOCK_STREAM = TCP/IP
"""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: # If no process is using the port,
    sock.bind(ADRESS) # the socket is bound to the specified adress:port (ex: 192.168.0.105:555)
    print('Server started, waiting for connection')
except:
    raise

def threaded_client(conn, client_id):  # This enables multiple clients to be handled at once
    
    conn.send(str(client_id).encode()) # Sends a player number token

    while not (client_data[0] == 'ready' and client_data[1] == 'ready'): # Waiting on both players to be ready
        client_data[client_id] = conn.recv(2048).decode('UTF-8')
        conn.sendall(b'not ready')

    conn.sendall(b'ready') # Start the game

    while True: # Communication loop between the client and the server
            data = conn.recv(2048).decode('UTF-8') # receive 2048 bytes at a time, decodes binary to text
            if data == 'exit': # Disconnection condition
                print('Client disconnected')
                conn.close() # close the connection to this client
                break

            else:
                print(data) # Shows message from the client
                reply = 'Message received: {}'.format(data) # Forms the reply
                conn.sendall(reply.encode()) # Send back the reply encoded to binary. Here, maybe send() does the job...


sock.listen(2) # Tells the socket to listen for up to 2 connection requests
client_data = ['', '']
client_id = 0 # The token identifying each individual client

while True <= 1: # Loop accepting the requests
    conn, addr = sock.accept() # accept() returns the connection and the ip:port of the client

    print('Connected by {0}:{1}'.format(addr[0], addr[1]))
    start_new_thread(threaded_client, (conn, client_id))
    client_id += 1 # Generate new token for the next client.
