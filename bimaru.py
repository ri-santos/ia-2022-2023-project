# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2
from copy import deepcopy
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
       #self.hints = np.empty(hintnum, dtype=object)

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
        if(type != 'W' and type != '.' and type != ' '):
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

        parse_board.hints = np.empty(hintnum, dtype=object)                      #podemos usar parse_board.hints fora desta funcao???

        for i in range(hintnum):
            hint = sys.stdin.readline().split()
            row = int(hint[1])
            col = int(hint[2])
            letter = hint[3]

            if letter == 'C' or letter == 'W':
                parse_board.fill_empty(row, col, letter)
            
            else: parse_board.hints[i] = np.array([row, col, letter])

            if letter != 'W':
                parse_board.water_around_boat(col, row, 1, 0) 

            if letter == 'T' or letter == 'M':
                parse_board.place_piece(row + 1, col, ' ')
            
            if letter == 'B' or letter == 'M':
                parse_board.place_piece(row -1, col, ' ')
            
            if letter == 'R' or letter == 'M':
                parse_board.place_piece(row, col + 1, ' ')
            
            if letter == 'L' or letter == 'M':
                parse_board.place_piece(row, col - 1, ' ')
            


        parse_board.place_water()
        return parse_board
    
    def fill_empty(self,row: int, col: int , type: str):
        if (self.get_value(row ,col) == ' '):
            self.place_piece(row,col,type)  


               # if (self.is_empty(idx,i)):
                #            self.place_piece(idx,i,'.')

    def place_water(self):
        zeros_rows = np.where(self.rows == 0)
        for elem in zeros_rows[0]:
            empty = np.where(self.board[elem] == ' ')
            for i in empty:
                self.place_piece(elem,i ,'.')
        zeros_cols = np.where(self.columns == 0)
        for i in range(10):
            for elem in zeros_cols[0]:
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

    def place_boat(self, x, y, size, direction):
        
        if direction == 0:
            self.fill_empty(y, x, 'l')
            for i in range(size-1):
                self.fill_empty(y, x+i, 'm')
                self.columns[x+i] -= 1
            self.fill_empty(y, x+size, 'r')
            
            self.columns[x] -= 1
            self.columns[x+size] -= 1
            self.rows[y] -= size


        else:
            self.fill_empty(y, x, 't')
            for i in range(size-1):
                self.fill_empty(y+i, x, 'm')
                self.columns[y+i] -= 1
            self.fill_empty(y+size-1, x, 'b')

            self.columns[y] -= 1
            self.columns[y+size] -= 1
            self.rows[x] -= size

        self.placed[size-1] += 1

        self.water_around_boat(x, y, size, direction)


    
    def get_hints(self):
        return self.hints

    def fits_boat(self,size):
        counter = 0  
        lista_posi = []

        fits = np.where(self.get_columns() >= size)
        
        for i in fits[0]:
            j = 0
            while j < 10:
                counter = 0
                l = j
                while l < 10:
                    slot = self.get_value(l,i)
                    if counter < size:
                        if (slot == ' '):
                            counter += 1
                            l+=1

                        else:
                            counter = 0
                            j = l + 1
                            break

                    elif (counter == size):
                        lista_posi.append([l - size , i])
                        break
                j+=1

        fits = np.where(self.get_rows() >= size)

        for i in fits[0]:
            j = 0
            while j < 10:
                counter = 0
                l = j
                while l < 10:
                    slot = self.get_value(i,l)
                    if counter < size:
                        if (slot == ' '):
                            counter += 1
                            l+=1

                        else:
                            counter = 0
                            j = l + 1
                            break

                    elif (counter == size):
                        lista_posi.append([i , l - size])
                        break
                j+=1

        return lista_posi
                    
                            
    


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

        actions = []

        if state_board.get_placed()[3] != 1:
            fits = np.where(state_board.get_columns() >= 4)
            size = 4
        elif state_board.get_placed()[2] != 2:
            fits = np.where(state_board.get_columns() >= 3)
            size = 3
        elif state_board.get_placed()[1] != 3:
            fits = np.where(state_board.get_columns() >= 2)
            size = 2
        elif state_board.get_placed()[0] != 4:
            fits = np.where(state_board.get_columns() >= 1)
            size = 1

        else: return ()

        print(state_board.fits_boat(4))
            


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

    # print("para as colu")
    print(board)
    print(board.fits_boat(4))
    board.place_boat(9, 0, 4, 1)
    board.water_around_boat(9,0,4,1)
    board.place_water()
    print(board)
   
    