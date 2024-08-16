from game.game import Game
from game.gameOfUr import GameOfUr
from game.checkers import Checkers
from player.player import Player
from player.human import Human
from player.bot import Bot
from util import getInput

from typing import Type

games: list[Type[Game] | None] = [None, GameOfUr, Checkers]
while True:
    
    print('select game:')
    for index, game in enumerate(games):
        print(f"{str(index)}: {"quit" if game == None else game.name}")
    gameChoice = games[int(getInput( lambda reply: reply in map(str, range(3)) ))]
    if gameChoice == None:
        quit()

    print('how many human players?')
    numHumans = gameChoice.numPlayers - int(getInput( 
        lambda reply: reply in map(str, range(gameChoice.numPlayers + 1)) 
    ))
    players: list[Player] = []
    for i in range(numHumans):
        players.append(Human())
    for i in range(gameChoice.numPlayers - numHumans):
        players.append(Bot())

    game = gameChoice(players)
    game.play()

    pass
