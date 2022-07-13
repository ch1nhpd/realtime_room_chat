import socket
import threading
import sys

from colorama import Fore, Back, Style

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print ("Correct usage: script IP address port number")
    exit()
host = str(sys.argv[1])
port = int(sys.argv[2])
client.connect((host, port))
# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK?' Send Nickname
            message = client.recv(1024).decode('utf-8')
            if message == 'WHAT IS YOUR NICK?':
                client.send(nickname.encode('utf-8'))
            else:
                print(Fore.GREEN +message)
                print(Style.RESET_ALL)
        except:
            # Close Connection When Error
            # print("An error occured!")
            client.close()
            sys.exit()
# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(nickname, input())
        client.send(message.encode('utf-8'))
        if message.split(': ')[1]=='exit!':
            client.close()
            sys.exit()
# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
sys.exit()