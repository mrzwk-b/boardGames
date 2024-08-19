from typing import Callable

def getInput(valid: Callable, prompt="", failMsg: str="invalid input") -> str:
    print(prompt)
    while True:
        reply = input()
        if valid(reply):
            break
        else:
            print(failMsg)
    return reply

def sign(x: int) -> int:
    if x == 0:
        return 0
    if x > 0:
        return 1
    if x < 0:
        return -1
    assert False
