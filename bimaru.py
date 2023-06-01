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

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
    
    def get_state_board(self):
        return self.board
    
    def copy_board(self):
        return self.get_board().copy_board()

    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, hints) -> None:
        self.board = np.full((10,10), fill_value=' ' ,dtype=np.str_)
        self.rows = np.empty(10)
        self.columns = np.empty(10)
        self.placed = [0,0,0,0]
        self.hints = hints

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

        

        rows = sys.stdin.readline().split()[1::]
        cols = sys.stdin.readline().split()[1::]

        hintnum = int(sys.stdin.readline())

        hints = np.empty(hintnum, dtype=object)                      #podemos usar parse_board.hints fora desta funcao???
        
        parse_board = Board(hints)
        parse_board.define_occupied(rows, cols)

        for i in range(hintnum):
            hint = sys.stdin.readline().split()
            row = int(hint[1])
            col = int(hint[2])
            letter = hint[3]

            if letter == 'C' or letter == 'W':
                parse_board.fill_empty(row, col, letter)
            
            else: parse_board.hints[i] = np.array([row, col, str(letter)])

            if letter != 'W':
                parse_board.water_around_boat(row, col, 1, 0) 

            if letter == 'T':
                parse_board.place_piece(row + 1, col, ' ')
                # parse_board.place_piece(row + 2, col - 1, '.')
                # parse_board.place_piece(row + 2, col + 1, '.')
                
            
            elif letter == 'B':
                parse_board.place_piece(row -1, col, ' ')
                # parse_board.place_piece(row - 2, col - 1, '.')
                # parse_board.place_piece(row - 2, col + 1, '.')
            
            elif letter == 'R':
                parse_board.place_piece(row, col + 1, ' ')
                # parse_board.place_piece(row - 1, col + 2, '.')
                # parse_board.place_piece(row + 1, col + 2, '.')
            
            elif letter == 'L':
                parse_board.place_piece(row, col - 1, ' ')
                # parse_board.place_piece(row - 1, col - 2, '.')
                # parse_board.place_piece(row + 1, col - 2, '.')

            elif letter == 'M':
                parse_board.place_piece(row + 1, col, ' ')
                parse_board.place_piece(row -1, col, ' ')
                parse_board.place_piece(row, col + 1, ' ')
                parse_board.place_piece(row, col - 1, ' ')

            
        parse_board.place_water()
        parse_board.hints = parse_board.hints[np.logical_not([element is None for element in parse_board.hints])]
        return parse_board
    
    def fill_empty(self,row: int, col: int , type: str):
        if (self.get_value(row ,col) == ' '):
            self.place_piece(row,col,type)  

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


    def water_around_boat(self, row, col, size, direction):

        left = col - 1 > -1
        top = row - 1 > -1

        if direction == 0:
            right = col + size < 10
            bottom = row + 1 < 10 


            if left: self.fill_empty(row, col-1, '.')

            if right: self.fill_empty(row, col+size, '.')

            if bottom:
                for i in range(size):
                    self.fill_empty(row+1, col+i, '.')
                if left: self.fill_empty(row+1, col-1, '.')
                if right: self.fill_empty(row+1, col+size, '.')
                
            if top:
                for i in range(size):
                    self.fill_empty(row-1, col+i, '.')
                if left: self.fill_empty(row-1, col-1, '.')
                if right: self.fill_empty(row-1, col+size, '.')

        
        elif direction == 1:
            right = col + 1 < 10
            bottom = row + size < 10 

            if left:
                for i in range(size):
                    self.fill_empty(row+i, col-1, '.')
                if top: self.fill_empty(row-1, col-1, '.')
                if bottom: self.fill_empty(row+size, col-1, '.')

            if right:
                for i in range(size):
                    self.fill_empty(row+i, col+1, '.')
                if top: self.fill_empty(row-1, col+1, '.')
                if bottom: self.fill_empty(row+size, col+1, '.')

            if bottom: self.fill_empty(row+size, col, '.')
            if top: self.fill_empty(row-1, col, '.')

    def place_boat(self, row, col, size, direction):
        
        if direction == 0:
            self.fill_empty(row, col, 'l')
            for i in range(size-1):
                self.fill_empty(row, col+i, 'm')
                self.columns[col+i] -= 1
            self.fill_empty(row, col+size, 'r')
            
            self.columns[col] -= 1
            self.columns[col+size-1] -= 1
            self.rows[row] -= size


        else:
            self.fill_empty(row, col, 't')
            for i in range(size-1):
                self.fill_empty(row+i, col, 'm')
                self.rows[row+i] -= 1
            self.fill_empty(row+size-1, col, 'b')

            self.rows[row] -= 1
            self.rows[row+size-1] -= 1
            self.columns[col] -= size

        self.placed[size-1] += 1

        self.water_around_boat(row, col, size, direction)

    
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

                    if (counter == size):
                        lista_posi.append([l - size , i, 1, size])
                        break
                j+=1

        fits = np.where(self.get_rows() >= size)
        print(fits)

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
                        lista_posi.append([i , l - size, 0, size])
                        break
                j+=1

        return lista_posi
                    
    def verify(self,row,column,direction):
        if direction == 0:
            counter = 0
            num = self.rows[row]
            for i in range(10):
                if self.get_value(row ,i) == ' ':
                    counter += 1
                if counter >= num:
                    break
            if counter < num:
                return False
            return True
        else:
            counter = 0
            num = self.columns[column]
            for i in range(10):
                if self.get_value(i,column) == ' ':
                    counter += 1
                if counter >= num:
                    break
            if counter < num:
                return False
            return True
        
    
    def verify_free_slots(self, row, col, size, direction):

        left = col - 1 > -1
        top = row - 1 > -1

        if direction == 0:
            right = col + size < 10
            bottom = row + 1 < 10 


            if left and not self.verify(row, col - 1, 1): return False

            if right and not self.verify(row, col + size, 1): return False

            if bottom and not self.verify(row + 1, col, 0): return False
                
            if top and not self.verify(row - 1, col, 0): return False

        
        elif direction == 1:
            right = col + 1 < 10
            bottom = row + size < 10 

            if left and not self.verify(row, col - 1, 1): return False

            if right and not self.verify(row, col + 1, 1): return False

            if bottom and not self.verify(row + size, col, 0): return False
                
            if top and not self.verify(row - 1, col, 0): return False

        return True


    # TODO: outros metodos da classe

class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

    #Result -> devolve board com o resultado -> vemos colunas/linhas adjacentes -> adicionamos ou não
        
        state_board = state.get_state_board()
        
        placed = state_board.get_placed()

        if placed[3] != 1:
            list_posi = state_board.fits_boat(4)
            size = 4
        elif placed[2] != 2:
            print('ON THREEEE')
            list_posi = state_board.fits_boat(3)
            size = 3
        elif placed[1] != 3:
            list_posi = state_board.fits_boat(2)
            size = 2
        elif placed[0] != 4:
            list_posi = state_board.fits_boat(1)
            size = 1

        else: return ()

        actions = list_posi
        print(list_posi)
        for elem in list_posi:
            row = elem[0]
            col = elem[1]
            direction = elem[2]
            size = elem[3]

            new_state = self.result(state , elem)
            new_state_board = new_state.get_state_board()

            if not new_state_board.verify_free_slots(row, col, size, direction): actions.remove(elem)

        return actions


    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        
        result_board = deepcopy(state.get_state_board())

        row = int(action[0])
        col = int(action[1])
        direction = int(action[2])
        size = int(action[3])

        if size == 1:
            result_board.fill_empty(row, col, "c")
        
        else:
            result_board.place_boat(row, col, size, direction)

        result_board.water_around_boat(row,col,size,direction)
        result_board.place_water()

        new_state = BimaruState(result_board)

        return new_state

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        state_board = state.get_state_board()

        hints = state_board.get_hints()
        placed = state_board.get_placed()

        print(state_board)
        counter = 4
        for i in hints:
            if state_board.get_value(int(i[0]), int(i[1])) == i[2].lower():
                state_board.place_piece(int(i[0]), int(i[1]), i[2])

            else: return False

        for i in placed:
            if i == counter:
                counter -= 1
            else: return False
        
        return True


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":

    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    problem = Bimaru(board)
    goal_node = depth_first_tree_search(problem)

    print(goal_node)
    
   
    