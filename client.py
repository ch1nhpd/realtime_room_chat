import socket
import threading
import sys
from AES_cipher import AESCipher

from colorama import Fore, Back, Style

aes = AESCipher()
nickname = input("Choose your nickname: ")

# if len(sys.argv) != 3:
#     print ("Correct usage: script IP address port number")
#     exit()
# host = str(sys.argv[1])
# port = int(sys.argv[2])
host = '127.0.0.1'
port = 55555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


def receive():
    while True:
        try:
            message = aes.decrypt(client.recv(1024).decode('utf-8'))
            if message == 'WHAT IS YOUR NAME?':
                client.send(aes.encrypt(nickname).encode('utf-8'))
            else:
                print(Fore.GREEN + message)
                print(Style.RESET_ALL)
        except:
            client.close()
            sys.exit()

def write():
    while True:
        message = '{}: {}'.format(nickname, input())
        client.send(aes.encrypt(message).encode('utf-8'))
        if message.split(': ')[1]=='exit!':
            client.close()
            sys.exit()

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
sys.exit()