import random

from core.player.bot import Bot
from gameOfUr.gameOfUrState import GameOfUrState as GouState

class GameOfUrBot(Bot):
    def decide(self, state: GouState, yBegin=0, xBegin=0, prompt=[], failMsg="") -> tuple[int, int]:
        preferred = []
        legal = []
        for row in range(3):
            for column in range(8):
                if state.isLegal((row, column)):
                    destination = state.moveDestination((row, column))
                    if destination in state.rosettes or state.board[destination] != 0:
                        preferred.append((row, column))
                    else:
                        legal.append((row, column))
        if len(legal) == 0:
            legal.append(())
        return random.choice(preferred if len(preferred) != 0 else legal)
