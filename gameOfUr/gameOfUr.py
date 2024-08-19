from core.game import Game
from .gameOfUrState import GameOfUrState as GouState
import random

class GameOfUr(Game):
    name = "Royal Game of Ur"
    numPlayers = 2
    reservedChars = {' ', '_', '|', '{', '}'}

    def __init__(self) -> None:
        super().__init__()
        self.state: GouState = GouState()
    
    def getRow(self, row: int) -> str:
        output = [['a','b','c'][row], ' ']
        for column in range(8):
            output.extend([
                ( # left wall
                        '{' 
                    if (row, column) in self.state.rosettes else 
                        ' ' 
                    if column in range(2,4) and row != 1 else 
                        '|'
                ), ( # piece, if present
                        ' '
                    if self.state.board[(row, column)] == 0 or (column in range(2,4) and row != 1) else 
                        self.players[self.state.board[(row, column)] == -1].symbol
                ), ( # right wall
                        '}' 
                    if (row, column) in self.state.rosettes else 
                        ' ' 
                    if column in range(2,4) and row != 1 else 
                        '|'
                )
            ])
        return ''.join(output) + '\n'

    def getBoard(self) -> str:
        output = "   1  2  3  4  5  6  7  8 \n"
        for row in range(3):
            output += self.getRow(row)
        scores = self.state.getScores()
        output += f"player 1 score: {scores[0]}\n"
        output += f"player 2 score: {scores[1]}\n"
        return output

    def play(self):
        turnIndex: int = 0 # used to index into self.players, marks whose turn it is
        while True:
            self.state.roll = sum([random.randint(0,1) for _ in range(4)])

            capture, rosette = self.state.resolveMove(self.players[turnIndex].decide(self.state,
                f'{self.getBoard()}'
                f'roll: {self.state.roll}\n'
                'enter one of the following:\n'
                '  "new" to send a new piece onto the board,\n'
                '  "pass" to skip your turn,\n'
                '  or the coordinates of a piece to move'
            ))

            if capture:
                self.state.sendHome()

            if self.state.getScores()[turnIndex] == 7:
                self.winnerIndex = turnIndex
                break

            if not rosette:
                turnIndex = 1 - turnIndex
                self.state.passTurn()

            self.state.sanityCheck()

        print(f"player {str(self.winnerIndex + 1)} wins!")
        scores = self.state.getScores()
        for i in range(2):
            print(f"player {str(i+1)} score: {scores[i]}\n")
