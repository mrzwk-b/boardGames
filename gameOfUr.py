import random
import gm
import numpy as np
import ai

def getBoard(p):
    global board
    st = ''
    for i in range(board[(0,3)]):
        st += p[0]
    st += '\n'
    st += '   1  2  3  4  5  6  7  8 \n'
    st += '   _  _        _  _  _  _ \n'
    for row in range(3):
        st += ['a','b','c'][row] + ' '
        for column in range(8):
            tile = (row,column)
            if board[tile] == 1:
                mid = p[0]
            elif board[tile] == -1:
                mid = p[1]
            else:
                mid = '_'
            if tile in rosette:
                wall = ['<','>']
            elif column in [2,3]:
                if row != 1:
                    wall = [' ',' ']
                if row == 2:
                    mid = ' '
                if row == 0:
                    mid = '_'
            else:
                wall = ['|','|']
            st += wall[0] + mid + wall[1]
            if column == 7:
                st += '\n'
    for j in range(abs(board[(2,3)])):
        st += p[1]
    return st

def checkMoves(roll):
    global board
    global turn
    global rosette
    legal = []
    sturn = [1,-1]
    if roll == 0:
        if disp:
            print('Player ' + str(turn + 1) + ': You rolled a 0 and can\'t move')
    else:
        if disp:
            print('Player ' + str(turn + 1) + ': You rolled a ' + str(roll))
        for i in range(3):
            for j in range(8):
                if (i != 1 and j == 2) or pnz((i,j)) != sturn[turn]:
                    # ensures you can't move a piece out of the end zone or an opponent's piece
                    continue
                dest = track((i,j),roll)
                if pnz(dest) == pnz((i,j)) and dest != (turn*2,2):
                    # ensures you can't move to a tile you already occupy
                    continue
                elif dest[0] == i and dest[1] > 2 and j < 3:
                    # ensures you can't move past the end zone
                    continue
                elif pnz(dest) == -1*pnz((i,j)) and dest in rosette:
                    # makes rosettes into safe spaces
                    continue
                elif (i,j) == (turn*2,3):
                    legal.append('new')
                else:
                    legal.append(['a','b','c'][i] + str(j+1))
    return legal,roll

def track(pos,roll):
    global turn
    if pos[0] == 1:
        if pos[1] - roll >= 0:
            dest = (1,pos[1]-roll)
        else:
            dest = (turn*2,(roll-pos[1])-1)
    else:
        if pos[1] + roll < 8:
           dest = (turn*2,pos[1]+roll)
        else:
            dest = (1,15-(roll+pos[1]))
    return dest

def resMove(play,p):
    global board
    global turn
    global aiTurn
    global rosette
    global disp
    if play[0] == None:
        return
    elif play[0] == 'new':
        move = (turn*2,3)
    else:
        move = (['a','b','c'].index(play[0][0]),int(play[0][1])-1)
    dest = track(move,play[1])
    if pnz(dest) == -1*pnz(move):
        board[(2*gm.opp(turn,2),3)] += pnz(dest)
        board[dest] = pnz(move)
        board[move] -= pnz(move)
    else:
        board[dest] += pnz(move)
        board[move] -= pnz(move)
    if dest in rosette:
        if disp:
            print('Extra turn!')
            print(getBoard(p))
        roll = random.randint(0,1)+random.randint(0,1)+random.randint(0,1)+random.randint(0,1)
        resMove(gm.getMove(checkMoves(roll),aiTurn,board,disp),p)    
    
def sanityCheck():
    global board
    global turn
    global score
    count = [0,0]
    for r in range(3):
        for c in range(8):
            if r != 1 and c in [2,3]:
                assert abs(board[(r,c)]) < 8,str((r,c)) + ' has more than 7 pawns \n' + str(board)
            else:
                assert abs(board[(r,c)]) < 2,str((r,c)) + ' has more than 1 pawn \n' + str(board)
            if board[(r,c)] > 0:
                count[0] += board[(r,c)]
            elif board[(r,c)] < 0:
                count[1] -= board[(r,c)]
    assert count == [7,7],'incorrect # of pawns: ' + str(count) + '\n' + str(board)
    for s in score:
        assert s >= 0,'score below 0: ' + score

def pnz(t):
    global board
    tile = board[t]
    if tile > 0:
        return 1
    elif tile < 0:
        return -1
    else:
        return 0

def gameplay(p,ais):
    global board
    global rosette
    global disp
    global turn
    global aiTurn
    global score
    board = np.zeros((3,8),int)
    board[(0,3)] += 7
    board[(2,3)] -= 7
    rosette = [(0,1),(0,7),(1,3),(2,1),(2,7)]
    if len(ais)  == 2:
        disp = False
    else:
        disp = True
    turn = 0
    score = [0,0]
    while True:
        if disp:
            print(getBoard(p))
        aiTurn = False
        for item in ais:
            if p[turn] == item.char:
                aiTurn = item
        roll = random.randint(0,1)+random.randint(0,1)+random.randint(0,1)+random.randint(0,1)
        resMove(gm.getMove(checkMoves(roll),aiTurn,board,disp),p)
        score = [board[(0,2)],-1*board[(2,2)]]
        if disp:
            print('Player 1\'s score: ' + str(score[0]))
            print('Player 2\'s score: ' + str(score[1]))
        sanityCheck()
        if score[0] == 7 or score[1] == 7:
            break
        turn = gm.opp(turn,2)
    for player in score:
        if player == 7:
            if disp:
                print('Player ' + str(score.index(player) + 1) + ' wins!')
            if len(ais) == 2:
                vict = score.index(7)
                losr = gm.opp(vict,2)
                ais[losr].evolve(score[losr]-7)
                ais[vict].evolve(7-score[losr])
        
