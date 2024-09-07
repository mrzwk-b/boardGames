from core.game import Game
from gameOfUr.gameOfUrBoard import GameOfUrBoard as GouBoard
from gameOfUr.gameOfUrState import GameOfUrState as GouState
from util import InputWindow

class GameOfUr(Game):
    name = "Royal Game of Ur"
    numPlayers = 2
    reservedChars = {' ', '_', '|', '$'} 

    def __init__(self, players) -> None:
        super().__init__(players)
        self.state: GouState = GouState()
        self.board: GouBoard = GouBoard(self.state, (self.players[0].symbol, self.players[1].symbol))

    def play(self):
        turnIndex: int = 0 # used to index into self.players, marks whose turn it is
        while True:
            self.state.reroll()

            onRosette = self.state.resolveMove(self.players[turnIndex].decide(
                self.state,
                yBegin = self.board.window.getmaxyx()[0],
                prompt = [
                    f'roll: {self.state.roll}',
                    'enter one of the following:',
                    '  "new" to send a new piece onto the board,',
                    '  "pass" to skip your turn,',
                    '  or the coordinates of a piece to move',
                ],
            ))

            if self.state.getScores()[turnIndex] == 7:
                self.winnerIndex = turnIndex
                break

            if not onRosette:
                turnIndex = 1 - turnIndex
                self.state.passTurn()

            self.state.sanityCheck()
            self.board.reflectState()

        self.board.reflectState()
        endDisplay = InputWindow(self.board.window.getmaxyx()[0], 0, [
            f"player {self.winnerIndex + 1} wins!",
             "press enter to continue"
        ])
        endDisplay.getInput(lambda reply: True)
        endDisplay.erase()
        self.board.erase()
