from re import T
import threading
import time
import sys
from tkinter import E
from functions import loader, validNickname, writeToFile
from socket import *
import os

nickname = validNickname()

if nickname == 'admin':
    password = input("Enter password\n")



# port = int(input("Choose Port > \n"))
# hostIp = input("Choose Ip Address >\n")
T_PORT = 3333
HOST = "127.0.0.1"  # localhost

client = socket(AF_INET, SOCK_STREAM)

conn = False
attempts = 0
while not conn:
    try:
        loader(3, "Loading")
        client.connect((HOST, T_PORT))
        conn = True
    except Exception as er:
        if attempts <= 1:
            attempts += 1
            print('Server not Found')
            time.sleep(1)
            continue
        else:
            print("      ABORT      ")
            time.sleep(2)
            os._exit(0)

stop_thread = False


def receive():
    while conn:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(2048).decode()
            if message == "NICK":
                client.send(nickname.encode())
                next_msg = client.recv(1024)
                if next_msg == "PASSWD":
                    client.send(password.encode())
                    if client.recv(1024).decode() == "REFUSE":
                        print(f"Wrong password, Connection Refused.")
                        stop_thread = True
            elif len(message) > 0:
                if "joined the chat!" in message:
                    print(message)
                elif f"Welcome to the sever {nickname}" in message:
                    print(message)
                else:
                    print(message)
        except Exception as e:
            print(f"\rAn Error occurred\n {e}")
            client.close()
            


def write():
    while 1:
        try:
            message = input("")
            if message.startswith('/'):
                print('Left The chat..')
                time.sleep(2)
                client.close()
            else:
                client.sendall(f"{nickname}: {message}".encode())
            time.sleep(0.2)
        except Exception as e:
            print("Server Closed!")
            print(e)
            os._exit(1)


if __name__ == "__main__":
    receive_threading = threading.Thread(target=receive)
    receive_threading.start()

    write_threading = threading.Thread(target=write)
    write_threading.start()
else:
    print("what the fuck did you try to do now? did you imported me?")
