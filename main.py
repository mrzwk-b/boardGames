from core.game import Game
from core.player.player import Player
from core.player.human import Human
from core.player.bot import Bot
from util import getInput
from org import games, bots
from typing import Type

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
        players.append(bots[gameChoice]())

    game = gameChoice()
    game.setup(players)
    game.play()

    pass
