from .player import Player
from util import getInput

class Human(Player):

    def pickSymbol(self, reservedChars: set[str]) -> str:
        print("choose a character to represent you")
        self.symbol = getInput(
            lambda reply: len(reply) == 1 and reply not in reservedChars,
            message=f"must not be element of {reservedChars}"
        )
        return self.symbol

    pass
