import curses

from core.state import State

class Board:
    window: curses.window
    state: State

    def __init__(
            self,
            state: State,
            ySize: int,    xSize: int=-1,
            yBegin: int=0, xBegin: int=0
        ) -> None:
        if xSize == -1:
            xSize = curses.COLS
        self.state = state
        self.window = curses.newwin(ySize, xSize, yBegin, xBegin)

    def erase(self):
        self.window.erase()
        self.window.refresh()

    def resize(self, ySize: int=-1, xSize: int=-1):
        pass # TODO

    def reposition(self, yBegin: int=-1, xBegin: int=-1):
        pass # TODO

    def reflectState(self):
        pass # implemented by child classes
