import socket
import threading



# Connection Data
host = '127.0.0.1'
port = 55555

# Sending Messages To All Connected Clients
def broadcast(message,clientSend=None):
    tmp = b'                         '
    for client in clients:
        if client != clientSend:
            client.send(tmp+message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            if message.decode('utf-8').split(': ')[1]=='exit!':
                a=1/0
            broadcast(message,client)
        except:
            # Removing And Closing Clients
            # print('ERROR!!!')
            index = clients.index(client)
            client.close()
            clients.remove(client)
            
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('utf-8'))
            print(nickname,' left!')
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('WHAT IS YOUR NICK?'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')

        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('utf-8'))
        client.send('Connected to server!'.encode('utf-8'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

print('SERVER IS RUNNING....')
receive()                