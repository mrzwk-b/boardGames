import curses
from core.board import grid
from core.board.board import Board
from gameOfUr.gameOfUrState import GameOfUrState as GouState

class GameOfUrBoard(Board):
    def __init__(self, state: GouState, symbols: tuple[str, str]) -> None:
        super().__init__(state, ySize=11, xSize=curses.COLS)
        self.state: GouState
        self.symbols = symbols
        self.boardWindow = self.window.derwin(8, 36, 0, (curses.COLS - 36) // 2)
        self.cellSize, offset = grid.drawGrid(self.boardWindow, (3, 8),
            rowNames=grid.AlphabeticCoordinates,
            colNames=grid.NumericCoordinates
        )
        # remove nonexistent tiles
        self.boardWindow.addch(offset[0], offset[1] + (self.cellSize[1] * 2), '┐')
        for y in range(offset[0], offset[0] + self.cellSize[0]):
            for x in range(offset[1] + (self.cellSize[1] * 2) + 1, offset[1] + (self.cellSize[1] * 4)):
                self.boardWindow.addch(y, x, ' ')
        self.boardWindow.addch(offset[0], offset[1] + (self.cellSize[1] * 4), '┌')
        self.boardWindow.addch(offset[0] + self.cellSize[0], offset[1] + (self.cellSize[1] * 3), '┬')
        self.boardWindow.addch(offset[0] + (self.cellSize[0] * 3), offset[1] + (self.cellSize[1] * 2), '┘')
        for y in range(offset[0] + (self.cellSize[0] * 2) + 1, offset[0] + (self.cellSize[0] * 3) + 1):
            for x in range(offset[1] + (self.cellSize[1] * 2) + 1, offset[1] + (self.cellSize[1] * 4)):
                self.boardWindow.addch(y, x, ' ')
        self.boardWindow.addch(offset[0] + (self.cellSize[0] * 3), offset[1] + (self.cellSize[1] * 4), '└')
        self.boardWindow.addch(offset[0] + (self.cellSize[0] * 2), offset[1] + (self.cellSize[1] * 3), '┴')
        # add rosettes
        for coordinates in self.state.rosettes:
            center = (
                offset[0] + (coordinates[0] * self.cellSize[0]) + 1,
                offset[1] + (coordinates[1] * self.cellSize[1]) + 2,
            )
            for side in [
                (center[0], center[1] - 2),
                (center[0], center[1] + 2),
                (center[0] - 1, center[1]),
                (center[0] + 1, center[1])
            ]:
                self.boardWindow.addch(side[0], side[1], '$')
        # add score section
        self.window.addstr(8,  (curses.COLS - 36) // 2, "scores:")
        self.window.addstr(9,  (curses.COLS - 36) // 2, "  player 1: 0")
        self.window.addstr(10, (curses.COLS - 36) // 2, "  player 2: 0")
        self.window.refresh()

    def reflectState(self) -> None:
        topLeft = (2, 4)
        for row in range(3):
            y = topLeft[0] + (row * self.cellSize[0])
            for col in range(8):
                if row != 1 and col in {2, 3}:
                    continue
                x = topLeft[1] + (col * self.cellSize[1])
                boardValue = self.state.board[(row, col)]
                self.boardWindow.addch(y, x,
                    self.symbols[1] if boardValue < 0 else
                    self.symbols[0] if boardValue > 0 else
                    ' '
                )
        self.boardWindow.refresh()
        self.window.addch(9, ((curses.COLS - 36) // 2) + 12, str(self.state.getScores()[0]))
        self.window.addch(10, ((curses.COLS - 36) // 2) + 12, str(self.state.getScores()[1]))
        self.window.refresh()
