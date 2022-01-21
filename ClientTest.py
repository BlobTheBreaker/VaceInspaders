from network import Network


# Little script to test it all.

n = Network() # Create a default Network obj which will connect to a server run from the same computer
n.connect() # Establishing connection

msg = ''

while msg != 'exit': # Communication loop with disconnection option
    msg = input('Send to server: ') 
    print(n.send(msg)) # "Print the response the server gave you when you sent this" 
                                                                    # -This Line