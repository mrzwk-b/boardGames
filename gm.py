# in the process of being eliminated from the project altogether

import random
import player.bot as bot


def opp(player, number):
    if player + 1 == number:
        return 0
    else:
        return player + 1

def getMove(moves,aiTurn,data,disp):
    legal = moves[0]
    if legal == []:
        if disp:
            print('No moves available')
        return None,moves[1]
    if not aiTurn:
        valid = False
        while not valid:
            print('Enter a move')
            play = input()
            if play not in legal:
                print('Not a valid move')
            else:
                valid = True
    else:
        play = aiTurn.think((data,moves[1]),moves[0])
    return play,moves[1]
