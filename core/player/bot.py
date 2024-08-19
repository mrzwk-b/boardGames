import random
from .player import Player

class Bot(Player):

    def pickSymbol(self, reservedChars: set[str]):
        self.symbol = random.choice(list({'!','@','#','$','%','^','&','*','?','+','=','~'} - reservedChars))
        return super().pickSymbol(reservedChars)

    def randMove(legal: set):
        return random.choice(list(legal))
