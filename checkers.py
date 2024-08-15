import random
import gm.pickPiece

def displayBoard(board, pawns):
    disp = '   _ _ _ _ _ _ _ _ \n'
    row = 0
    while row < 8:
        disp += (str(row + 1) + ' |')
        for tile in board[(row)]:
            if tile > 0:
                disp += pawns[0] + '|'
            elif tile < 0 :
                disp += pawns[1] + '|'
            else:
                disp += '_|'
        disp += '\n'
        row += 1
    return disp
        

def winCondition(board):
    piece = 0
    i = 0
    j = 0
    while i < 8:
        while j < 8:
            if board[(i,j)] == 0:
                j+= 1
                continue
            elif piece == 0:
                piece = board[(i,j)]
            elif (board[(i,j)] > 0) != (piece > 0):
                return False
            j += 1
        j = 0
        i += 1
    return True


def legal(board, turn):
    #establish frame of reference for processing the board based on turn
    if turn = 1:
        piece = -1
    else:
        piece = 1
        field = []
        for row in board[::-1]:
            field.append(row[::-1])
    #set up lists of possible moves
    violent = []
    peaceful = []
    #iterate over every single piece and every direction it could move in
    for row in range(8):
        for column in range(8):
            #get range of motion for piece
            if board[row][column] == piece:
                dirs = [[1], [-1,1]]
            else if board[row][column] == piece * 2:
                dirs = [[-1,1], [-1,1]]
            else:
                continue
            #prune to prevent out of bounds exceptions
            if row == 0:
                dirs[0] = [1]
            else if row == 7:
                dirs[0] = [-1]
            if column == 0:
                dirs[1] = [1]
            else if column == 7:
                dirs[1] = [-1]
            #figure out what's over there
            for fb in dirs[0]:
                for lr in dirs[1]:
                    if board[row + fb][column + lr] == -piece or board[row + fb][column + lr] == -piece * 2:
                        if row + (2 * fb) > -1 and row + (2 * fb) < 8 and column + (2 * lr) > -1 and column + (2 * lr) < 8:
                            if board[row + (2 * fb)][column + (2 * lr)] == 0:
                                violent.append(((row, column), (2 * fb, 2 * lr)))
                    else if board[row + fb][column + lr] == 0:
                        peaceful.append(((row, column), (fb, lr)))
    if len(violent) > 0:
        return violent
    else:
        return peaceful
                                
                        
    


def getMove(board, turn):
    if turn == 0:
        valid = False
        while not valid:
            move = input()
            if move in legal(board, turn):
                valid = true
            else:
                print('Not a valid move')
        return move
    else:
        return random.choice(legal(board, turns))


board = [[-1,0,-1,0,-1,0,-1,0],
         [0,-1,0,-1,0,-1,0,-1],
         [-1,0,-1,0,-1,0,-1,0],
         [0,0,0,0,0,0,0,0],
         [0,0,0,0,0,0,0,0],
         [0,1,0,1,0,1,0,1],
         [1,0,1,0,1,0,1,0],
         [0,1,0,1,0,1,0,1]]

pawns = pickPiece(2,0)[0]
turn = 0
while not winCondition(board):
    print(displayBoard(board, pawns))
    print('Player ' + str(turn + 1) + ': your move')
    move = getMove(board, turn)
    
    
        
