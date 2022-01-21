from network import Network

n = Network()
n.connect()

msg = ''

while msg != 'exit':
    msg = input('Send to server: ')
    print(n.send(msg))