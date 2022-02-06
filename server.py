import sys
from socket import *
import threading
import time
from functions import timeNow, writeToFile


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
                if message == '/chat':
                    if len(self.nicknames) > 2:
                        client.send(f'{", ".join(self.nicknames[:-1])} and {self.nicknames[-1]} is in the chat'.encode())
                    elif len(self.nicknames) == 1:
                        client.send(f'Its only you {self.nicknames[0]}'.encode())
                    else:
                        client.send(f'{self.nicknames[0]} and {self.nicknames[1]} is in the chat.'.encode())
                elif message == '/help':
                    helpMsg = """
                    Hello There !
                    to see all members in the chat enter '/chat'.
                    for help enter '/help'.
                    """
                    client.send(helpMsg.encode())
                else:
                    self.broadcast(message)
            except Exception as e:
                print(e)
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

                    if input('Continue Listening? ') == 'y':
                        sys.stdout.write("\nServer is listening....")
                    else:
                        print(f"Ended at {timeNow()}")
                        totalRunTime = int(time.perf_counter() - self.startTime)
                        print(f"Total run time - {totalRunTime} Seconds.")
                        self.serverSocket.close()
                        sys.exit(0)
                break
            except KeyboardInterrupt:
                self.serverSocket.close()
                break

    def receive(self):
        while True:
            try:
                client, address = self.serverSocket.accept()
                print(f"Connected with {str(address)}")

                client.send("NICK".encode())
                nickname = client.recv(2048).decode()

                if nickname == "Admin":
                    client.send("PASSWD".encode())
                    passwd = client.recv(1024).decode()

                    if passwd != "adminpass":
                        client.send("REFUSE".encode())
                        client.close()
                        continue

                self.nicknames.append(nickname)
                self.clients.append(client)

                if nickname == "Admin":
                    print("Admin Connected to the server !")
                else:
                    print(f"The nickname is {nickname}")
                self.broadcast(f"--> {nickname} joined the chat! <--")
                client.send(f"Welcome to the sever {nickname}".encode())

                handleThreading = threading.Thread(target=self.handle, args=(client,))
                handleThreading.start()

                print(f"active connections {threading.active_count() - 1}")
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

time.sleep(10)