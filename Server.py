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
    
    conn.send('Hello Client {0}'.format(client_id).encode()) # Sends a visual confirmation of the connection

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
client_id = 1 # The token identifying each individual client

while True: # Loop accepting the requests
    conn, addr = sock.accept() # accept() returns the connection and the ip:port of the client

    print('Connected by {0}:{1}'.format(addr[0], addr[1]))

    """
    Here, we hand over the connection to each client to a different subprocess with the function 
    'start_new_process', which will run the function 'threaded_client' with the arguments in the tuple.
    This subprocess will output in the same terminal as Server.py but will allow the server accepting
    requests and each individual server-client exchange to happen simultaneously.
    """

    start_new_thread(threaded_client, (conn, client_id))
    client_id += 1 # Generate new token for the next client
