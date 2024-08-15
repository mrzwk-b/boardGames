import random
import ai

def opp(player, number):
    if player + 1 == number:
        return 0
    else:
        return player + 1

def pickPiece(count,aiNum):
    players = []
    ais = []
    p = 0
    while p < count - aiNum:
        invalid = True
        while invalid:
            print('Player ' + str(p + 1) + ': Enter your symbol')
            chose = input()
            if len(chose) > 1:
                print('it\'s 1 character only you greedy ho')
            else:
                if chose in players:
                    print('that one\'s taken')
                else:
                    players.append(chose)
                    p += 1
                    invalid = False
    while p < count:
        invalid = True
        while invalid:
            chose = random.choice([';','#','$','&','*','@','%','^','!','?','+','=','<','>','~','-'])
            if chose not in players:
                players.append(chose)
                valid = False
                while not valid:
                    iD = random.randint(0,99)
                    if iD not in [item.char for item in ais]:
                        valid = True                        
                ais.append(ai.Jeur(iD,players.index(chose),chose))
                p += 1
                invalid = False
    return (players,ais)

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
