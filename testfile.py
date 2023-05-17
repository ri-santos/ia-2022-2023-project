import numpy as np
from sys import stdin

if __name__ == "__main__":
    board = np.full((10,10), dtype=np.str_, fill_value=".")
    line1 = stdin.readline().split()[1::]
    line2 = stdin.readline().split()[1::]
    print(line1)
    
    hintnum = int(stdin.readline())

    for i in range(hintnum):
        hint = stdin.readline().split()
        board[int(hint[1])][int(hint[2])] = hint[3]

    
    boardstring = ""
    for i in range(10):
        board_row = " ".join(board[i])
        boardstring += board_row + "\n"


    print(boardstring)

