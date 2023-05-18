import numpy as np
from sys import stdin

if __name__ == "__main__":
    board = np.empty((10,10), dtype=np.str_)
    line1 = stdin.readline().split()[1::]
    line2 = stdin.readline().split()[1::]
    print(line1)
    
    hintnum = int(stdin.readline())

    for i in range(hintnum):
        hint = stdin.readline().split()
        row = int(hint[1])
        col = int(hint[2])
        piece = hint[3]
        if piece.lower() == "t":
            if 0 < row:
                board[row-1][col-1:col+2] = "."
            if row < 9:
                board[row+1][col-1] = "."
                board[row+1][col+1] = "."
            if 0 < col:
                board[row][col-1] = "."
                board[row][col+1] = "."

        
        board[row][col] = piece

    
    boardstring = ""
    for i in range(10):
        board_row = " ".join(board[i])
        boardstring += board_row + "\n"


    print(boardstring)

