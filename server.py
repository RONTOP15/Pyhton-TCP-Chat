from socket import *
import threading
import time
from functions import timeNow, writeToFile, handleCommands


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
        print(f"Server listening in port {self.port}\n")

    def broadcast(self, message):
        for cli in self.clients:
            cli.sendall(f"{message}".encode())
        self.msgs.append(f"[{timeNow()}] - {message}")

    def handle(self, client):
        while True:
            try:
                msg = message = client.recv(2048).decode()
                if msg.startswith('/'):
                    handleCommands(msg, self.msgs, client, self.nicknames)
                elif msg.startswith("KICK"):
                    try:
                        nickToKick = msg[11:].capitalize()
                        self.kickUser(nickToKick)
                    except:
                        continue
                else:
                    self.broadcast(message)
            except Exception as e:
                print(f"{self.nicknames[self.clients.index(client)]} Disconnected!")
                clientIndex = self.clients.index(client)
                self.clients.remove(client)
                client.close()

                nickname = self.nicknames[clientIndex]
                self.broadcast(f"<- {nickname} has left the chat :( ->")
                self.nicknames.remove(nickname)

                if len(self.clients) == 0:
                    print('No More Clients')
                    # Saves chat history
                    writeToFile(self.msgs)
                    self.msgs = []
                    if input('Continue Listening? ') == 'y':
                        print("\nServer is listening....\n")
                    else:
                        print(f"Ended at {timeNow()}")
                        totalRunTime = int(time.perf_counter() - self.startTime)
                        print(f"Total run time - {totalRunTime} Seconds.")
                        self.serverSocket.close()
                        break

                break
            except KeyboardInterrupt:
                self.serverSocket.close()
                break

    def kickUser(self, name):
        if name in self.nicknames:
            nicknameIndex = self.nicknames.index(name)
            clientToKick = self.clients[nicknameIndex]
            clientToKick.send("You have been kick by an admin!".encode())
            clientToKick.close()
            self.broadcast(f'{name} has been kicked by an admin!')
        else:
            print('nickname is not in the list')

    def receive(self):
        while True:
            try:
                client, address = self.serverSocket.accept()

                client.send("NICK".encode())
                nickname = client.recv(2048).decode()
                if nickname == "Admin":
                    client.send("PASSWD".encode())
                    passwd = client.recv(1024).decode()
                    if passwd != "123":
                        client.send("REFUSE".encode())
                        print(f"Failed to connect as Admin by {str(address)}")
                        client.close()
                        continue

                print(f"Connected with {str(address)}")

                self.broadcast(f"--> {nickname} joined the chat! <--")
                self.nicknames.append(nickname)
                self.clients.append(client)

                print(f"{nickname} Connected to the server!")
                client.send(f"Welcome to the sever {nickname}".encode())

                handleThreading = threading.Thread(target=self.handle, args=(client,))
                handleThreading.start()

            except Exception as e:
                print(e)
                break
            except KeyboardInterrupt:
                self.serverSocket.close()
                break


if __name__ == "__main__":
    server = Server("0.0.0.0", 3333)
    server.bind()
    server.receive()

time.sleep(3)
