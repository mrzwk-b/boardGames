import random
import numpy as np

from core.state import State
from util import sign

class GameOfUrState(State):
    board: np.ndarray
    rosettes: set[tuple[int, int]]
    roll: int
    turnIndex: int

    def __init__(self):
        # define board and put all pieces on their starts
        self.board = np.zeros((3,8),int)
        self.rosettes = {(0,1), (0,7), (1,4), (2,1), (2,7)}
        self.board[(0,3)] += 7
        self.board[(2,3)] -= 7
        # player 1's turn
        self.turnIndex = 1

    def passTurn(self):
        self.turnIndex *= -1

    def friendlySide(self) -> int:
        """
        returns the row index of the side of the board accessible to the current player
        """
        return 1 - self.turnIndex

    def moveDestination(self, start: tuple[int, int]) -> tuple[int, int] | None:
        """
        takes a start point and uses [self.roll] to calculate where a piece there ends up
        """
        # in middle
        if start[0] == 1:
            # to middle
            if (start[1] - self.roll) >= 0:
                return (1, start[1] - self.roll)
            # to edge
            else:
                # past end
                if self.roll == 4 and start == (1,0):
                    return None
                # successful
                else:
                    return (self.friendlySide(), self.roll - (start[1] + 1))
        # on edge
        else:
            # start 
            if start[1] >= 3:
                # to edge still
                if start[1] + self.roll <= 7:
                    return (start[0], start[1] + self.roll)
                # to middle
                else:
                    return(1, 15 - (start[1] + self.roll))
            # end
            else:
                # past end
                if start[1] + self.roll >= 3:
                    return None
                # successful
                else:
                    return (start[0], start[1] + self.roll)
    
    def parseMove(self, move: str) -> tuple[int, int] | tuple[()] | None:
        if move == 'pass':
            return ()
        if move == 'new':
            return (self.friendlySide(), 3)
        elif len(move) != 2:
            return None
        else:
            return (ord(move[0]) - ord('a'), ord(move[1]) - ord('1'))

    def isLegal(self, origin: tuple[int, int] | tuple[()] | None) -> bool:
        if origin == ():
            return True
        if origin == None:
            return False
        destination = self.moveDestination(origin)
        return (
            # origin is in the board
            origin[0] in range(3) and
            origin[1] in range(8) and
            # destination exists
            destination != None and
            # the relevant player actually has a piece there
            sign(self.board[origin]) == self.turnIndex and
            # doesn't land on ally unless it's the goal space
            (
                True if destination == (self.friendlySide(), 2) 
                else sign(self.board[destination]) != self.turnIndex
            ) and
            # doesn't land on safe enemy
            (True if self.board[destination] == 0 else destination not in self.rosettes)
        )

    def resolveMove(self, move: tuple[int, int] | tuple[()]) -> tuple[bool, bool]:
        """
        takes coordinates for the start and end of the move,
        returns bool indicating whether a rosette was landed on
        """
        if move == ():
            return (False, False)
        destination = self.moveDestination(move)
        # pick up piece from origin
        self.board[move] -= self.turnIndex
        # determine if a capture occurs and send that piece home if so
        if self.board[destination] != 0 and destination != (self.friendlySide(), 2):
            self.board[destination] = 0
            self.board[(2 - self.friendlySide(), 3)] -= self.turnIndex
        # place piece at destination
        self.board[destination] += self.turnIndex
        return destination in self.rosettes

    def sanityCheck(self):
        pawnCounts = [0,0]
        for row in range(3):
            for column in range(8):
                if row != 1 and column in [2,3]:
                    assert \
                        abs(self.board[(row,column)]) < 8, \
                        f"{str((row,column))} has more than 7 pawns\n{str(self.board)}"
                else:
                    assert \
                        abs(self.board[(row,column)]) < 2, \
                        f"{str((row,column))} has more than 1 pawn\n{str(self.board)}"
                if self.board[(row,column)] != 0:
                    pawnCounts[0 if sign(self.board[(row,column)]) == 1 else 1] += abs(self.board[(row,column)])
        assert \
            pawnCounts == [7,7], \
            f"incorrect # of pawns: {str(pawnCounts)}\n{str(self.board)}"

    def getScores(self) -> tuple[int, int]:
        return (self.board[0,2], -self.board[2,2])
    
    def reroll(self):
        self.roll = sum([random.randint(0,1) for _ in range(4)])
