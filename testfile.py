import numpy as np
from sys import stdin

if __name__ == "__main__":
    board = np.full((10,10), fill_value= ' ', dtype=np.str_)
    line1 = stdin.readline().split()[1::]
    line2 = stdin.readline().split()[1::]
    print(line1)
    
    hintnum = int(stdin.readline())

    for i in range(hintnum):
        hint = stdin.readline().split()
        row = int(hint[1])
        col = int(hint[2])

        piece = hint[3]          
            
        
        board[row][col] = piece
        
        if(board[row-1][col-1] == ' '):
            board[row-1][col-1] = '.'

    
    boardstring = ""
    for i in range(10):
        board_row = " ".join(board[i])
        boardstring += board_row + "\n"


    print(board)

