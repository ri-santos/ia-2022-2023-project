# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from operator import index
from re import X
import sys
import numpy as np
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self) -> None:
        self.board = np.full((10,10), fill_value=' ' ,dtype=np.str_)
        self.rows = np.empty(10)
        self.columns = np.empty(10)

    def __str__(self) -> str:
        # boardstring = ""
        # for i in range(10):
        #     board_row = "".join(self.board[i])
        #     boardstring += board_row +  "\n"
        
        # return boardstring
        return str(self.board)
    
    def define_occupied(self, rows, cols):
        self.rows = np.array(rows, dtype=np.int64)
        self.columns = np.array(cols, dtype=np.int64)

    def change_occupied_posi(self,row: int ,col: int):
        num = int(self.rows[row])
        self.rows[row] = str(num - 1) 
        num = int(self.columns[col])
        self.columns[col] = str(num - 1) 

    def place_piece(self, row: int, col: int, type: str):
        self.board[row, col] = type
        if(type != 'W' and type != '.'):
            self.change_occupied_posi(row,col)
        

    def get_value(self, row: int, col: int) -> str:
        """Devolve o valor na respetiva posição do tabuleiro."""
        
        return str(self.board[row][col])

    def adjacent_vertical_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        
        return (self.get_value(row-1, col), self.get_value(row+1, col))

    def adjacent_horizontal_values(self, row: int, col: int) -> (str, str):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        return (self.get_value(row, col-1), self.get_value(row, col+1))
    
    def copy_board(self):
        return np.copy(self.board)
    
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """

        parse_board = Board()

        rows = sys.stdin.readline().split()[1::]
        cols = sys.stdin.readline().split()[1::]
        
        parse_board.define_occupied(rows, cols)

        hintnum = int(sys.stdin.readline())

        parse_board.hints = np.empty(hintnum, dtype=object)

        for i in range(hintnum):
            hint = sys.stdin.readline().split()
            if hint[3] == 'C' or hint[3] == 'W':
                parse_board.place_piece(int(hint[1]), int(hint[2]), hint[3])
                parse_board.simplify_board(int(hint[1]), int(hint[2]), hint[3])

            else: parse_board.hints[i] = np.array([hint[1], hint[2], hint[3]])

        return parse_board
    
    def fill_empty(self,row: int, col: int , type: str):
        if (self.get_value(row ,col) == ' '):
            self.place_piece(row,col,type)  


               # if (self.is_empty(idx,i)):
                #            self.place_piece(idx,i,'.')

    def place_water(self, list:str):
        idx = 0
        if (list == 'r'): 
            zeros = np.where(self.rows == 0)
            for elem in zeros[0]:
                empty = np.where(self.board[elem] == '')
                for i in empty:
                    self.place_piece(elem,i ,'.')
        else:
            zeros = np.where(self.columns == 0)
            for i in range(10):
                for elem in zeros[0]:
                    self.fill_empty(i, elem,'.')                     


    def simplify_right_circle(self,row: int, col: int):
                                               #estar no meio
        self.fill_empty(row , col + 1 , '.')
        self.fill_empty(row + 1, col , '.')
        self.fill_empty(row + 1, col + 1 , '.')


    def simplify_right_top(self,row: int, col: int):
                                               #estar no meio
        self.fill_empty(row , col + 1 , '.')
        self.fill_empty(row - 1, col , '.')

    def simplify_right_bottom(self,row: int, col: int):
                                               #estar no meio
        self.fill_empty(row + 1 , col, '.')
        self.fill_empty(row, col + 1, '.')


    def simplify_right_left(self,row: int, col: int):
                                               #estar no meio
        self.fill_empty(row + 1 , col, '.')
        self.fill_empty(row - 1, col , '.')

    def simplify_left_circle(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row - 1, col , '.')
        self.fill_empty(row , col - 1 , '.')
        self.fill_empty(row + 1, col , '.')

    def simplify_left_top(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row - 1, col , '.')
        self.fill_empty(row , col - 1 , '.')
    
    def simplify_left_bottom(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row + 1, col , '.')
        self.fill_empty(row , col - 1 , '.')

    def simplify_left_right(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row + 1, col , '.')
        self.fill_empty(row - 1 , col, '.')


    def simplify_bottom_circle(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row + 1, col , '.')
        self.fill_empty(row  , col -1, '.')
        self.fill_empty(row , col + 1, '.')

    def simplify_bottom_right(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row + 1, col , '.')
        self.fill_empty(row , col + 1, '.')

    def simplify_bottom_left(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row + 1, col , '.')
        self.fill_empty(row , col -  1, '.')

    def simplify_bottom_top(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row, col + 1 , '.')
        self.fill_empty(row , col -  1, '.')

    def simplify_above_circle(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row - 1, col  , '.')
        self.fill_empty(row , col -  1, '.')
        self.fill_empty(row , col + 1, '.')

    def simplify_above_right(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row - 1, col  , '.')
        self.fill_empty(row , col + 1, '.')

    def simplify_above_left(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row - 1, col  , '.')
        self.fill_empty(row , col - 1, '.')

    def simplify_above_bottom(self,row: int, col: int):                    #se  estiver no meio
        self.fill_empty(row, col + 1 , '.')
        self.fill_empty(row , col - 1, '.')


    def simplify_around(self,row: int, col: int):
        self.fill_empty(row + 1, col + 1 , '.')
        self.fill_empty(row + 1, col - 1 , '.')
        self.fill_empty(row - 1, col + 1 , '.')
        self.fill_empty(row - 1, col - 1 , '.')

    def simplify_around_left(self,row: int, col: int):
        self.fill_empty(row + 1, col , '.')
        self.fill_empty(row , col - 1 , '.')
        self.fill_empty(row - 1, col , '.')

    def simplify_around_top(self,row: int, col: int):
        self.fill_empty(row , col + 1 , '.')
        self.fill_empty(row , col - 1 , '.')
        self.fill_empty(row - 1, col , '.')

    def simplify_around_bottom(self,row: int, col: int):
        self.fill_empty(row + 1, col , '.')
        self.fill_empty(row , col - 1 , '.')
        self.fill_empty(row , col + 1 , '.')

    def simplify_around_right(self,row: int, col: int):
        self.fill_empty(row + 1, col , '.')
        self.fill_empty(row - 1, col , '.')
        self.fill_empty(row , col + 1 , '.')
        

    def auxiliar_simplify_board(self,row: int, col: int , type :str):
        self.simplify_around(row,col)

        if (type == 'C' or type == 'c'):
            self.simplify_around_left(row, col)
            self.fill_empty(row , col + 1 , '.')
    
        elif((type == 'T' or type == 't')):
            self.simplify_around_top(row, col)

        elif((type == 'B' or type == 'b')):
            self.simplify_around_bottom(row, col)
        
        elif((type == 'L' or type == 'l')):
            self.simplify_around_left(row, col)
        
        elif((type == 'R' or type == 'r')):
            self.simplify_around_right(row, col)
    
    def simplify_board(self,row: int, col: int,type: str):
        if(type != 'W' or type != 'w'):
            if(((col - 1) == -1) and (col == 0)):           #1 coluna
                if((row - 1) == -1):           #estar canto esq superior
                    if (type == 'C' or type == 'c'):
                        self.fill_empty(row + 1, col , '.')
                        self.fill_empty(row + 1, col + 1 , '.')
                        self.fill_empty(row , col + 1 , '.')

                        # self.simplify_right_circle(row,col)
                    elif((type == 'T' or type == 't')):
                        self.fill_empty(row + 1, col + 1 , '.')
                        self.fill_empty(row , col + 1 , '.')
                    
                    else:
                        if((type == 'L' or type == 'l')):
                            self.fill_empty(row + 1, col , '.')
                            self.fill_empty(row + 1, col + 1 , '.')
                elif((row + 1) == 10):        #estar canto esq inferior
                    if (type == 'C' or type == 'c'):
                        self.fill_empty(row - 1, col , '.')
                        self.fill_empty(row - 1, col + 1 , '.')
                        self.fill_empty(row , col + 1 , '.')

                    elif((type == 'B' or type == 'b')):
                        self.fill_empty(row - 1, col - 1 , '.')
                        self.fill_empty(row , col + 1 , '.')
                    
                    else:
                        if((type == 'L' or type == 'l')):
                            self.fill_empty(row - 1, col , '.')
                            self.fill_empty(row - 1, col + 1 , '.')
                else:
                    self.fill_empty(row + 1, col + 1, '.')
                    self.fill_empty(row - 1, col + 1 , '.')
                    if (type == 'C' or type == 'c'):
                        self.simplify_right_circle(row, col)
                    
                    elif (type == 'T' or type == 't'):
                        self.simplify_right_top(row, col)

                    elif((type == 'M' or type == 'm')):
                        self.fill_empty(row, col + 1 , '.')

                    elif((type == 'B' or type == 'b')):
                        self.simplify_right_bottom(row, col)
                    
                    else:       
                        if((type == 'L' or type == 'l')):
                            self.simplify_right_left(row, col)

            elif(((col + 1) == 10)and (col == 9)):           #10 coluna

                if((row - 1) == -1):           #estar canto dir superior
                    self.fill_empty(row + 1, col - 1 , '.')

                    if (type == 'C' or type == 'c'):
                        self.fill_empty(row + 1, col , '.')
                        self.fill_empty(row , col - 1 , '.')
                    
                    elif((type == 'R' or type == 'r')):
                        self.fill_empty(row + 1, col, '.')
                    
                    else:
                        if((type == 'T' or type == 't')):
                            self.fill_empty(row, col - 1, '.')
            

                elif((row + 1) == 10):        #estar canto dir inferior

                    self.fill_empty(row - 1, col - 1 , '.')

                    if (type == 'C' or type == 'c'):
                        self.fill_empty(row - 1, col , '.')
                        self.fill_empty(row , col - 1 , '.')

                    elif((type == 'B' or type == 'b')):
                        self.fill_empty(row, col - 1 , '.')
            
                    else:
                        if((type == 'R' or type == 'r')):
                            self.fill_empty(row - 1, col , '.')

                else:
                    self.fill_empty(row - 1, col - 1, '.')
                    self.fill_empty(row + 1, col - 1 , '.')

                    if (type == 'C' or type == 'c'):
                        self.simplify_left_circle(row, col)
                    
                    elif (type == 'T' or type == 't'):
                        self.simplify_left_top(row, col)

                    elif((type == 'M' or type == 'm')):
                        self.fill_empty(row, col - 1 , '.')

                    elif((type == 'B' or type == 'b')):
                        self.simplify_left_bottom(row, col)
                    
                    else:       
                        if((type == 'R' or type == 'r')):
                            self.simplify_left_right(row, col)



            elif(((row + 1) == -1)and ( 0 < col < 9)):           #1 linha 
                    self.fill_empty(row + 1, col - 1, '.')
                    self.fill_empty(row  + 1, col + 1 , '.')

                    if (type == 'C' or type == 'c'):
                        self.simplify_bottom_circle(row,col)
                    
                    elif((type == 'R' or type == 'r')):
                        self.simplify_bottom_right(row,col)

                    elif((type == 'M' or type == 'm')):
                        self.fill_empty(row + 1, col, '.')

                    elif((type == 'L' or type == 'l')):
                        self.simplify_left_bottom(row, col)
                    
                    elif((type == 'T' or type == 't')):
                        self.simplify_left_top(row, col)


            elif(((row + 1) == 10)and ( 0 < col < 9)):           #10 linha 
                    self.fill_empty(row - 1, col - 1, '.')
                    self.fill_empty(row - 1, col + 1 , '.')

                    if (type == 'C' or type == 'c'):
                        self.simplify_above_circle(row,col)
                    
                    elif((type == 'R' or type == 'r')):
                        self.simplify_above_right(row,col)

                    elif((type == 'M' or type == 'm')):
                        self.fill_empty(row - 1, col, '.')

                    elif((type == 'L' or type == 'l')):
                        self.simplify_above_left(row, col)
                    
                    elif((type == 'B' or type == 'b')):
                        self.simplify_above_bottom(row, col)
                
            else:                                                #estao no meio 
                self.auxiliar_simplify_board(row, col , type)

    # TODO: outros metodos da classe

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    
    def get_board(self):
        return self.board
    
    def copy_board(self) -> Board:
        return self.get_board().copy_board()

    # TODO: outros metodos da classe

class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        result_board = state.copy_board()
        x = action[0]
        y = action[1]
        boat = action[2]
        direction = action[3]

        if boat == 1:
            result_board.fill_empty(x, y, "c")
            result_board.simplify_board(x, y, "c")

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":

    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()


   
    board.place_water('r')
    print("para as linhas")

    print(board)


    print("(8,8)")
    print(board.get_value(8,8))

    print("(8,7)")
    print(board.get_value(8,7))

    print("(8,9)")
    print(board.get_value(8,9))

    print("(9,9)")
    print(board.get_value(9,9))

    print("(8,9)")
    print(board.get_value(8,9))

    print("(7,9)")
    print(board.get_value(7,9))

    print("(7,7)")
    print(board.get_value(7,9))

    print("(7,8)")
    print(board.get_value(7,8))






    board.place_water('c')
    print("para as colu")
    print(board)

    print("(0,1)")
    print(board.get_value(0,1))

    print("(1,0)")
    print(board.get_value(1,0))
   
    # Imprimir valores adjacentes

    print(board.adjacent_vertical_values(3, 3))
    print(board.adjacent_horizontal_values(3, 3))
    print(board.adjacent_vertical_values(1, 0))
    print(board.adjacent_horizontal_values(1, 0))
    print(board.get_value(0, 0))