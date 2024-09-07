import curses
from typing import Callable

class InputWindow:
    window: curses.window

    def __init__(self, yBegin, xBegin, prompt: list[str]) -> None:
        self.window = curses.newwin(3 + len(prompt), curses.COLS, yBegin, xBegin)
        self.window.border()
        for i, line in enumerate(prompt):
            self.window.addstr(i + 1, 1, line)

    def getInput(self, isValid: Callable[[str], bool], failMsg: Callable[[str], str] | str="invalid input"):
        curses.curs_set(2)
        curses.echo()
        while True:
            reply = self.window.getstr(self.window.getmaxyx()[0] - 2, 1).decode("utf-8")
            if isValid(reply):
                curses.curs_set(0)
                curses.noecho()
                return reply
            else:
                alert = failMsg if type(failMsg) is str else failMsg(reply)
                self.window.addstr(
                    self.window.getmaxyx()[0] - 1,
                    curses.COLS - (len(alert) + 1),
                    alert
                )
                for x in range(1, curses.COLS - 1):
                    self.window.addch(self.window.getmaxyx()[0] - 2, x, ' ')
                self.window.refresh()

    def erase(self):
        self.window.erase()
        self.window.refresh()

def sign(x: int) -> int:
    if x == 0:
        return 0
    if x > 0:
        return 1
    if x < 0:
        return -1
    assert False
