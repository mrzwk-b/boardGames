from .player.player import Player
from .state import State
# from player.human import Human
import random

class Game:
    name: str
    numPlayers: int | range
    reservedChars: set[str]
    state: State

    def __init__(self) -> None:
        pass

    def setup(self, players: list[Player]):
        self.players = players
        # self.display = False
        for player in players:
            self.reservedChars.add(player.pickSymbol(self.reservedChars))
            # if type(Player) is Human:
            #     self.display = True
        random.shuffle(self.players)
        pass
    
    def play(self):
        pass

    pass
