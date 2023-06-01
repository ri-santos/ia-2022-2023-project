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

            # if left:
            #     if not top and not bottom:
            #         if direction == 0:
                        
            #             if new_state_board.verify(row - 1,col,0) == True and new_state_board.verify(row + 1,col,0)== True and new_state_board.verify(row ,col + 1,0) and verify:
            #                 actions += [elem]
                    
            #         else:
            #             if new_state_board.verify(row - 1,col,1) == True and new_state_board.verify(row + size,col,1)== True and new_state_board.verify(row ,col + 1,1) and verify:
            #                 actions += [elem]
            # if top:
            #     if direction == 0:
            #         if new_state_board.verify(row + 1,col,0)== True and new_state_board.verify(row ,col + 1,0) and verify:
            #             actions += [elem]
                
            #     else:
            #         if right:
            #             if new_state_board.verify(row,col + 1,1) == True  and new_state_board.verify(row + size ,col,1)== True and verify:
            #                 actions += [elem]
            #         if left:
            #             if new_state_board.verify(row,col - 1,1) == True  and new_state_board.verify(row + size ,col,1)== True and verify:
            #                 actions += [elem]
                            

            # if bottom:
            #     if direction == 0:
            #         if new_state_board.verify(row - 1,col,0)== True and new_state_board.verify(row ,col + 1,0) and verify and new_state_board.verify(row ,col - 1,0):
            #             actions += [elem]
                
            #     elif direction == 1:
            #         if right:
            #             if not top and new_state_board.verify(row,col + 1,1) == True  and new_state_board.verify(row - size ,col,1)== True and verify:
            #                 actions += [elem]
            #         if left:
            #             if not top and new_state_board.verify(row,col - 1,1) == True  and new_state_board.verify(row - size ,col,1)== True and verify:
            #                 actions += [elem]

    
    boardstring = ""
    for i in range(10):
        board_row = " ".join(board[i])
        boardstring += board_row + "\n"


    print(board)

