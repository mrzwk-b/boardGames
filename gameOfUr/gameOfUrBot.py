from core.state import State
from .gameOfUrState import GameOfUrState as GouState
from core.player.bot import Bot
import random

class GameOfUrBot(Bot):
    def decide(self, state: GouState, prompt: str = "") -> tuple[int, int]:
        legal = []
        for row in range(3):
            for column in range(8):
                if state.isLegal((row, column)):
                    legal.append((row, column))
        if len(legal) == 0:
            legal.append(())
        return random.choice(legal)

    