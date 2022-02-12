import sys
import time
from datetime import datetime, date
import re
import os


def timeNow(*args):
    now = datetime.now()
    today = date.today()
    if args:
        if args[0] == 'f':
            return now.strftime("%H%M%S")
        if args[0] == 'd':
            return today.strftime('%d-%m-%y')
    else:
        return now.strftime("%H:%M:%S")


def loader(*args):
    a = 0
    for a in range(0, args[0]):
        a = a + 1
        b = (f"{args[1]}" + "." * a)
        sys.stdout.write('\r' + b)
        time.sleep(0.5)
    return sys.stdout.write("\r")


def validNickname():
    while True:
        nickname = input('Choose Nickname : ').capitalize()
        try:
            if re.match("^[a-zA-Z]+.*", nickname):
                if ' ' in nickname:
                    print("Nickname can't contain spaces")
                elif re.compile('[@_!#$%^\'&*(;)<>?/\]\[|}{~:]').search(nickname):
                    print("Special Characters are not allowed")
                elif len(nickname) <= 3:
                    print('Nickname too short, minimum 3 chars')
                    continue
                elif len(nickname) > 12:
                    print('Nickname too long, max 12 chars')
                    continue
                else:
                    return nickname
            else:
                print("Nickname must begin with letters")
                continue
        except Exception as e:
            print(e)
            return sys.exit(0)
        else:
            continue


def writeToFile(msgs):
    save = input('Save chat history ? [Y/N]> ').lower()
    if save == "y":
        filename = f"./logs/{timeNow('d')}/{timeNow('f')}-chat.log"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w') as file:
            for message in msgs:
                file.write(f'{message} \n')
        return sys.stdout.write(f"Saved to file {timeNow('f')}\n")
    else:
        return sys.stdout.write("\n Chat history not saved.\n")


def handleCommands(msg, msgs, client, nicknames):
    if msg == '/who':
        if len(nicknames) > 2:
            client.send(
                f'{", ".join(nicknames[:-1])} and {nicknames[-1]} is in the chat'.encode())
        elif len(nicknames) == 1:
            client.send(f'Its only you {nicknames[0]}'.encode())
        else:
            client.send(f'{nicknames[0]} and {nicknames[1]} is in the chat.'.encode())
    elif msg == "/his":
        his = ''
        for i in msgs:
            his += f"{i}\n"
        client.send(his.encode())
    else:
        client.send(f'No command named - "{msg}"'.encode())


if __name__ == '__main__':
    pass
