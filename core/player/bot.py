import random

from core.player.player import Player

class Bot(Player):
    def randMove(legal: set):
        return random.choice(list(legal))
