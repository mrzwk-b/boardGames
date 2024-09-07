import random

from core.player.player import Player
from core.player.human import Human
from core.state import State

class SymbolChoiceState(State):
    """state that can be passed to decide to allow players to choose their character"""
    taken: set[str]

    def __init__(self, reserved: set[str]) -> None:
        super().__init__()
        self.taken = reserved

    def parseMove(self, move: str) -> str:
        """returns the symbol chosen, no need for processing"""
        return move
    
    def isLegal(self, move: str) -> bool:
        return len(move) == 1 and move not in self.taken

class Game:
    name: str
    numPlayers: int | range
    reservedChars: set[str]
    state: State
    players: list[Player]

    def __init__(self, players: list[Player]) -> None:
        self.players = players
        symbolSelector = SymbolChoiceState(self.reservedChars)
        symbolChoice: str
        for player in players:
            if type(player) is Human:
                symbolChoice = player.decide(symbolSelector, 
                    0, 0, [
                        "choose a symbol to represent you", 
                        "the following are unavailable",
                        ', '.join([f"'{s}'" for s in symbolSelector.taken])
                    ]
                )
            else:
                symbolChoice = random.choice(list(
                    {'!','@','#','$','%','^','&','*','?','+','=','~'} - symbolSelector.taken
                ))
            player.symbol = symbolChoice
            symbolSelector.taken.add(symbolChoice)
        random.shuffle(self.players)
    
    def play(self):
        pass
