from player.player import Player
# from player.human import Human

class Game:
    name: str
    numPlayers: int | range
    reservedChars: set[str]

    def __init__(self, players: list[Player]) -> None:
        self.players = players
        # self.display = False
        for player in players:
            self.reservedChars.add(player.pickSymbol(self.reservedChars))
            # if type(Player) is Human:
            #     self.display = True
        
        pass

    def play(self):
        pass

    pass
