import sys
import threading
import time
from functions import loader, validNickname, writeToFile
from socket import *
import os

nickname = validNickname()
if nickname == "Admin":
    password = input("Enter Password : ")

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
    except:
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
                next_msg = client.recv(1024).decode()
                if next_msg == "PASSWD":
                    client.send(password.encode())
                    if client.recv(1024).decode() == "REFUSE":
                        print(f"Wrong password, Connection Refused.")
                        stop_thread = True
                        client.close()
            else:
                print(message)

        except ConnectionAbortedError:
            print("Disconnected Successfully!")
            break
        except Exception as e:
            print(f"\rAn Error occurred\n {e}")
            client.close()
            break


def write():
    while True:
        if stop_thread:
            break
        try:
            message = input("")
            if message.startswith('/'):
                if message.startswith('/exit'):
                    print('Left The chat..')
                    time.sleep(2)
                    client.close()
                    break
                else:
                    client.send(message.encode())
            else:
                client.sendall(f"{nickname}: {message}".encode())
            time.sleep(0.2)
        except Exception as e:
            print("Server Closed!")
            print(e)
            break


if __name__ == "__main__":
    receive_threading = threading.Thread(target=receive)
    receive_threading.start()

    write_threading = threading.Thread(target=write)
    write_threading.start()
else:
    print("what the fuck did you try to do now? did you imported me?")
