import curses
from typing import Callable

class CoordinateNamingScheme:
    def __init__(self):
        self.value = None
        self.increment = lambda _: None

    def next(self):
        """
        returns the current value of the counter and then increments it
        """
        temp = self.value
        self.value = self.increment(self.value)
        return temp

class AlphabeticCoordinates(CoordinateNamingScheme):
    def __init__(self):
        super().__init__()
        self.value = 'a'
        self.increment = lambda x: chr(ord(x) + 1)

class NumericCoordinates(CoordinateNamingScheme):
    def __init__(self):
        super().__init__()
        self.value = '1'
        self.increment = lambda x: str(int(x) + 1)

def generateRow(cellCount: int, cellWidth: int, strokes: tuple[str, str, str, str]) -> str:
    """
    [cellWidth] represents interior size of cells

    [strokes] holds characters for (left wall, middle walls, interiors, right wall)
    """
    return \
        f"{strokes[0]}" \
        f"{strokes[1].join([strokes[2] * cellWidth for _ in range(cellCount)])}" \
        f"{strokes[3]}"

def drawGrid(
    window: curses.window,
    boardDimensions: tuple[int, int],
    labelCoordinates: bool = True,
    rowNames: type[CoordinateNamingScheme] = NumericCoordinates,
    colNames: type[CoordinateNamingScheme] = AlphabeticCoordinates,
) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    draws a uniform rectangular grid in the window provided
    (requires an empty column at the end because curses is terrible)

    returns a tuple of tuples indicating 
        the y,x dimensions of a cell and 
        the y,x offsets from coordinate labelling
    
    the total height and width of the board will be 
    congruent to 1 mod the respective cell dimensions
    
    [boardDimensions]: (rows, columns)

    [rowNames] and [colNames] are ignored if [labelCoordinates] is false
    """
    yOffset = 1 if labelCoordinates else 0
    xOffset = 2 if labelCoordinates else 0
    cellSize = (
        (window.getmaxyx()[0] - yOffset - 1) // boardDimensions[0],
        (window.getmaxyx()[1] - xOffset - 2) // boardDimensions[1]
    )

    # column labels
    if labelCoordinates:
        colNames = colNames()
        rowNames = rowNames()
        for col in range(boardDimensions[1]):
            window.addch(0, xOffset + 1 + ((cellSize[1] - 1) // 2) + (col * cellSize[1]), colNames.next())
    
    # rows loop
    for y in range(yOffset, window.getmaxyx()[0]):
        # row labels
        if labelCoordinates and (y - yOffset) % cellSize[0] == cellSize[0] // 2:
            window.addstr(y, 0, f'{rowNames.next()} ')
        # main row
        strokes = \
            ('┌', '┬', '─', '┐') if y == yOffset else \
            ('└', '┴', '─', '┘') if y == window.getmaxyx()[0] - 1 else \
            ('├', '┼', '─', '┤') if (y - yOffset) % (cellSize[0]) == 0 else \
            ('│', '│', ' ', '│')
        row = generateRow(boardDimensions[1], cellSize[1] - 1, strokes)
        window.addstr(y, xOffset, row)
    window.refresh()
    return (cellSize, (yOffset, xOffset))
