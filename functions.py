import sys
import time
from datetime import datetime
import re

def timeNow(*args):
    now = datetime.now()
    if args:
        if args[0] == 'f':
            return now.strftime("%H%M%S")
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
        nickname = input('Choose Nickname :  ')
        try:
            if re.match("^[a-zA-Z]+.*",nickname):
                if ' ' in nickname:
                    print("Nickname can't contain spaces")
                elif len(nickname) <= 3:
                        print('Nickname too short')
                        continue
                else:
                    return nickname
            else:
                print("Nickname must begin with letters")
                continue
        except:
            return sys.exit(0)
        
        
def writeToFile(msgs):
    save = input('Save chat history ? [Y/N]> ').lower()
    if save == "y":
        with open(f'./logs/{timeNow("f")}-chat.log', 'w') as file:
            for message in msgs:
                file.write(f'{message} \n')
        return sys.stdout.write("DONE")
    else:
        return sys.stdout.write('\nChat history not saved.')