from typing import Callable

def getInput(valid: Callable, message="invalid input") -> str:
    while True:
        reply = input()
        if valid(reply):
            break
        else:
            print(message)
    return reply