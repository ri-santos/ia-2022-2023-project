# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2
from copy import deepcopy
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
        self.placed = [0,0,0,0]

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
    
    def get_placed(self):
        return self.placed
    
    def get_rows(self):
        return self.rows
    
    def get_columns(self):
        return self.columns

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
                parse_board.fill_empty(int(hint[1]), int(hint[2]), hint[3])
                if hint[3] == 'C':
                    parse_board.water_around_boat(int(hint[2]), int(hint[1]), 1, 0)

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
                empty = np.where(self.board[elem] == ' ')
                for i in empty:
                    self.place_piece(elem,i ,'.')
        else:
            zeros = np.where(self.columns == 0)
            for i in range(10):
                for elem in zeros[0]:
                    self.fill_empty(i, elem,'.')                     


    def water_around_boat(self, x, y, size, direction):

        left = x - 1 > -1
        top = y - 1 > -1

        if direction == 0:
            right = x + size < 10
            bottom = y + 1 < 10 


            if left: self.fill_empty(y, x-1, '.')

            if right: self.fill_empty(y, x+size, '.')

            if bottom:
                for i in range(size):
                    self.fill_empty(y+1, x+i, '.')
                if left: self.fill_empty(y+1, x-1, '.')
                if right: self.fill_empty(y+1, x+size, '.')
                
            if top:
                for i in range(size):
                    self.fill_empty(y-1, x+i, '.')
                if left: self.fill_empty(y-1, x-1, '.')
                if right: self.fill_empty(y-1, x+size, '.')

        
        elif direction == 1:
            right = x + 1 < 10
            bottom = y + size < 10 

            if left:
                for i in range(size):
                    self.fill_empty(y+i, x-1, '.')
                if top: self.fill_empty(y-1, x-1, '.')
                if bottom: self.fill_empty(y+size, x-1, '.')

            if right:
                for i in range(size):
                    self.fill_empty(y+i, x+1, '.')
                if top: self.fill_empty(y-1, x+1, '.')
                if bottom: self.fill_empty(y+size, x+1, '.')

            if bottom: self.fill_empty(y+size, x, '.')
            if top: self.fill_empty(y-1, x, '.')

    def place_boat(self, x, y, size, direction, hint, hint_data):
        if hint:
            self.fill_empty(hint_data[0], hint_data[1], hint_data[2])
        
        if direction == 0:
            self.fill_empty(y, x, 'l')
            for i in range(size):
                self.fill_empty(y, x+i, 'm')
                self.columns[x+i] -= 1
            self.fill_empty(y, x+size, 'r')
            
            self.columns[x] -= 1
            self.columns[x+size] -= 1
            self.rows[y] -= size


        else:
            self.fill_empty(y, x, 't')
            for i in range(size):
                self.fill_empty(y+i, x, 'm')
                self.columns[y+i] -= 1
            self.fill_empty(y+size, x, 'b')

            self.columns[y] -= 1
            self.columns[y+size] -= 1
            self.rows[x] -= size

        self.placed[size-1] += 1


    
    def get_hints(self):
        return self.hints

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
        state_board = state.get_board()

        if state_board.get_placed()[3] != 4:
            fits4 = np.where(state_board.get_columns() >= 4)

            for i in fits4:
                hint_col = np.where(state_board.get_hints()[1] == i)
            
            



    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        result_board = deepcopy(state.get_board())

        x = int(action[0])
        y = int(action[1])
        size = int(action[2])
        direction = int(action[3])
        hint = action[4]
        hint_data = action[5]

        if size == 1:
            result_board.fill_empty(x, y, "c")
        
        else:
            result_board.place_boat(x, y, size, direction, hint, hint_data)

        result_board.water_around_boat(x,y,size,direction)

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
    board.place_water('c')
    # print("para as colu")
    print(board)
   
    # Imprimir valores adjacentes

    print(board.adjacent_vertical_values(3, 3))
    print(board.adjacent_horizontal_values(3, 3))
    print(board.adjacent_vertical_values(1, 0))
    print(board.adjacent_horizontal_values(1, 0))
    print(board.get_value(0, 0))