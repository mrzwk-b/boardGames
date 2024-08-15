import random
import numpy as np
import os
import shelve
import math

class Jeur:
    
    def __init__(self,iD,turn,char):
        db = shelve.open('minds')
        self.iD = str(iD)
        self.turn = turn
        self.char = char
        self.ioso = db[self.iD]
        db.close()

    def think(self,data,legal):
        enput = []
        for i in range(3):
            if self.turn:
                for j in data[0][2-i]:
                    enput.append(-1*j)
            else:
                for j in data[0][i]:
                    enput.append(j)
        enput.append(data[1])
        for layr in range(int(len(self.ioso)/2)):
            exput = []
            nron = 0
            while nron < len(self.ioso[layr*2]):
                valu = 0
                for cnxn in range(len(self.ioso[layr*2][nron])):
                    valu += self.ioso[layr*2][nron][cnxn]*enput[cnxn]
                valu += self.ioso[(layr*2)+1][nron]
                exput.append(1/(1 + math.exp(-valu)))
                nron += 1
            if (layr*2)+2 == len(self.ioso):
                assert len(exput) == 16, print('last layer has ' + str(len(exput)) + ' neurons \n output layer:' + str(exput))
                valid = False
                while not valid:
                    choice = max(exput)
                    if exput.index(choice) < 8:
                        tile = (self.turn*2,exput.index(choice))
                    else:
                        tile = (1,exput.index(choice)-8)
                    move = ['a','b','c'][tile[0]] + str(tile[1] + 1)
                    if move in ['a4','c4']:
                        move = 'new'
                    if move in legal:
                        valid = True
                    else:
                        exput[exput.index(choice)] = 0
            else:
                enput = exput
        assert move in legal, print('illegal move:' + move)
        return move
            

    def evolve(self,score):
        db = shelve.open('minds')
        if score < 0:
            del db[self.iD]
        else:
            rep = []
            for layr in range(int(len(self.ioso)/2)):
                repWeights = self.ioso[layr*2]
                for x in np.nditer(repWeights, op_flags = ['readwrite']):
                    x += np.random.normal()/4
                repBiases = self.ioso[(layr*2)+1]
                for x in repBiases:
                    x += np.random.normal()/4
                rep.extend([repWeights,repBiases])
            for i in range(100):
                if str(i) not in db:
                    db[str(i)] = rep

    
def brandNew():
    minds = shelve.open('minds')
    for i in range(100):
        net = []
        j = random.randint(1,3)
        for k in range(j+1):
            if k == 0:
                weights = np.empty((random.randint(7,35),25))
            elif k == j:
                weights = np.empty((16,len(net[-2])))
            else:
                weights = np.empty((random.randint(7,35),len(net[-2])))
            biases = []
            for r in range(len(weights)):
                biases.append(round(np.random.normal(),4))
                for c in range(len(weights[r])):
                    weights[(r,c)] = round(np.random.normal(),6)
            net.append(weights)
            net.append(biases)
        minds[str(i)] = net
    minds.close()
    

def randMove(legal):
    ops = []
    for m in legal:
        if m not in ops:
            ops.append(m)
    move = random.choice(ops)
    return move

