import email
import sys
from socket import *
import threading
from turtle import st
import time
from functions import timeNow
import os

class Server(object):
    def __init__(self, host, port):
        self.startTime = time.perf_counter()
        self.host, self.port = host, port
        self.clients, self.nicknames = [], []
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.msgs = []

    def bind(self):
        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(5)
        print(f"Started at {timeNow()}")
        sys.stdout.write(f"Server listening in port {self.port}\n")


    def broadcast(self, message):
        for cli in self.clients:
            cli.sendall(f"{message}".encode())
        self.msgs.append(f"[{timeNow()}] - {message}")

    def handle(self, client):
        while True:
            try:
                message = client.recv(2048).decode()
                self.broadcast(message)
            except Exception as e:
                print(e)
                clientIndex = self.clients.index(client)
                self.clients.remove(client)
                client.close()

                nickname = self.nicknames[clientIndex]
                self.broadcast(f"{nickname} has left the chat.")
                self.nicknames.remove(nickname)
                if len(self.clients) == 0:
                    print('No More Clients')
                    self.writeToFile()
                    if input('Continue Listening? ') == 'y':
                        sys.stdout.write("Server is listening....")
                    else:
                        print(f"Ended at {timeNow()}")
                        endTime = time.perf_counter()
                        total = int(endTime - self.startTime)
                        print(f"Total run time - {total} Seconds.")
                        os._exit(0)
                break

    def receive(self):
        while True:
            try:
                client, address = self.serverSocket.accept()
                print(f"Connected with {str(address)}")

                client.send("NICK".encode())
                nickname = client.recv(2048).decode()


                if nickname == "admin":
                    client.send("PASSWD".encode())
                    passwd = client.recv(1024).decode()
                    if passwd != "adminpass":
                        client.send("REFUSE".encode())
                        client.close()
                        continue

                
                self.nicknames.append(nickname)
                self.clients.append(client)

                
                print(f"The nickname is {nickname}")
                self.broadcast(f"{nickname} joined the chat!")
                client.send(f"Welcome to the sever {nickname}".encode())

                handleThreading = threading.Thread(target=self.handle, args=(client,))
                handleThreading.start()

                print(f"active connections {threading.active_count() - 1}")
            except Exception as e:
                sys.stderr.write(str(e))
                continue



    def writeToFile(self):
        save = input('Save chat history ? [Y/N]> ').lower()
        if save == "y":
            with open(f'./logs/{timeNow("f")}-chat.log', 'a+') as file:
                for message in self.msgs:
                    file.write(f'{message} \n')
            sys.stdout.write("\rDONE")
        else:
            print('Chat history not saved.')


if __name__ == "__main__":
    server = Server("0.0.0.0", 3333)
    server.bind()
    server.receive()
