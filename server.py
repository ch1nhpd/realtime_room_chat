import socket
import threading
from AES_cipher import AESCipher


host = '127.0.0.1'
port = 55555
clients = []
nicknames = []
accounts = ['user1','user2','user3','user4']


def login(username):
    if username in accounts and username not in nicknames:
        return True
    return False

def broadcast(message,clientSend=None):
    pad = '                         '
    for client in clients:
        if client != clientSend:
            client.send(aes.encrypt(pad + message).encode('utf-8'))


def handle(client):
    while True:
        try:
            message = aes.decrypt(client.recv(1024).decode('utf-8'))
            if message.split(': ')[1]=='exit!':
                a=1/0
            broadcast(message,client)
        except:
            index = clients.index(client)
            client.close()
            clients.remove(client)
            
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname))
            print(nickname,' left!')
            nicknames.remove(nickname)
            break

def receive():
    while True:

        client, address = server.accept()
        print("Connected with {}".format(str(address)))


        client.send(aes.encrypt('WHAT IS YOUR NAME?').encode('utf-8'))
        nickname = aes.decrypt(client.recv(1024).decode('utf-8'))

        if login(nickname):
            nicknames.append(nickname)
            clients.append(client)

            print("Nickname is {}\n".format(nickname))
            broadcast("{} joined!".format(nickname))
            client.send(aes.encrypt('Connected to server!').encode('utf-8'))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        else:
            client.close()
            

aes = AESCipher()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()
print('SERVER IS RUNNING....')
receive()                