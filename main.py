import gameOfUr as gOU
import checkers
import ai
import gm
import numpy as np
import random

games = ['Game of Ur','Checkers']
while True:
    print('Select game:')
    for item in games:
        print(str(games.index(item) + 1) + ': ' + item)
    valid = False
    while not valid:
        game = input()
        if game in ['1','2']:
            game = int(game) - 1
            valid = True
        else:
            print('Please enter the number of the option you want')
    print('Select mode: \n p: Play \n t: Train')
    valid = False
    while not valid:
        mode = input()
        if mode == 'p':
            valid = True
        elif mode == 't':
            if game == 0:
                valid == True
            else:
                print('Training mode not available for ' + games[game])
        else:
            print('Please enter either "p" or "t"')
    if game == 0:
        if mode == 'p':
            print('How many players?')
            valid = False
            while not valid:
                aiNum = 2 - int(input())
                if aiNum in range(2):
                    valid = True
                else:
                    print('Please enter either 1 or 2')
            (p,ais) = gm.pickPiece(2,aiNum)
            gOU.gameplay(p,ais)
        elif mode == 't':
            print('How many cycles?')
            valid = False
            while not valid:
                cycles = input()
                try:
                    cycleNum = int(cycles)
                    valid = True
                except:
                    print('Not a valid input')
            for i in range(cycleNum):
                print('Now beginning cycle ' + str(i + 1))
                jeurs = list(range(100))
                pairs = []
                for j in range(50):
                    a = random.choice(jeurs)
                    jeurs.remove(a)
                    b = random.choice(jeurs)
                    jeurs.remove(b)
                    pairs.append((a,b))
                for j in pairs:
                    pA = ai.Jeur(a,0,'a')
                    pB = ai.Jeur(b,1,'b')
                    gOU.gameplay(('a','b'),(pA,pB))
            print('Training finished')
    elif game == 1:
        print('How many players?')
        valid = False
        while not valid:
            aiNum = 2 - int(input())
            if aiNum in range(2):
                valid = True
            else:
                print('Please enter either 1 or 2')
        (p,ais) = gm.pickPiece(2,aiNum)
        checkers.gameplay(p,ais)
