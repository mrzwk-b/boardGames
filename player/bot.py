import random
from .player import Player

class Bot(Player):

    def pickSymbol(self, reservedChars: set[str]):
        self.symbol = random.choice(list({'!','@','#','$','%','^','&','*','?','+','=','~'} - reservedChars))
        return super().pickSymbol(reservedChars)

    def randMove(legal):
        options = []
        for m in legal:
            if m not in options:
                options.append(m)
        move = random.choice(options)
        return move
