# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 28:
# 102787 Ricardo Santos
# 104195 Sofia Du


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

    
    def __str__(self) -> str:
        return str(self.board)


    def __lt__(self, other):
        return self.id < other.id


    def get_state_board(self):
        return self.board


    def copy_board(self):
        return self.get_board().copy_board()


    def get_id(self):
        return self.id


class Board:
    """Representação interna de um tabuleiro de Bimaru."""

    def __init__(self, hints) -> None:
        self.board = np.full((10,10), fill_value=' ' ,dtype=np.str_)
        self.rows = np.empty(10)
        self.columns = np.empty(10)
        self.placed = np.array([4,3,2,1])
        self.hints = hints


    def __str__(self) -> str:
        boardstring = ""
        for i in self.board:
            board_row = ''.join(i)
            boardstring += "".join(board_row) +  "\n"
        return boardstring


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


    def replace_piece(self, row: int, col: int, type: str):
        self.board[row, col] = type


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
        hints = np.empty(hintnum, dtype=object)                
        
        parse_board = Board(hints)
        parse_board.define_occupied(rows, cols)

        for i in range(hintnum):
            hint = sys.stdin.readline().split()
            row = int(hint[1])
            col = int(hint[2])
            letter = hint[3]

            if letter == 'C' or letter == 'W':
                parse_board.fill_empty(row, col, letter)
                if letter == 'C':
                    parse_board.placed[0] -= 1
            else: parse_board.hints[i] = np.array([row, col, str(letter)])

            if letter != 'W':
                parse_board.water_around_boat(row, col, 1, 0) 

            if letter == 'T':
                parse_board.place_piece(row + 1, col, ' ')
                if row + 2 < 10:
                    if col - 1 > -1:
                        parse_board.place_piece(row + 2, col - 1, '.')
                    if col + 1 < 10:
                        parse_board.place_piece(row + 2, col + 1, '.')
                
            elif letter == 'B':
                parse_board.place_piece(row - 1, col, ' ')
                if row - 2 > -1:
                    if col - 1 > -1:
                        parse_board.place_piece(row - 2, col - 1, '.')
                    if col + 1 < 10:
                        parse_board.place_piece(row - 2, col + 1, '.')
            
            elif letter == 'R':
                parse_board.place_piece(row, col - 1, ' ')
                if col - 2 > -1:
                    if row - 1 > -1:
                        parse_board.place_piece(row - 1, col - 2, '.')
                    if row + 1 < 10:
                        parse_board.place_piece(row + 1, col - 2, '.')
            
            elif letter == 'L':
                parse_board.place_piece(row, col + 1, ' ')
                if col + 2 < 10:
                    if row - 1 > -1:
                        parse_board.place_piece(row - 1, col + 2, '.')
                    if row + 1 < 10:
                        parse_board.place_piece(row + 1, col + 2, '.')

            elif letter == 'M':
                if row + 1 < 10:
                    parse_board.place_piece(row + 1, col, ' ')
                if row - 1 > -1:
                    parse_board.place_piece(row - 1, col, ' ')
                if col + 1 < 10:
                    parse_board.place_piece(row, col + 1, ' ')
                if col - 1 > -1:
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
        if size == 1: self.fill_empty(row, col, 'c')
        else:
            if direction == 0:
                self.fill_empty(row, col, 'l')
                i = 1
                while i < size-1:
                    self.fill_empty(row, col+i, 'm')
                    i+=1
                self.fill_empty(row, col+size-1, 'r')
            else:
                self.fill_empty(row, col, 't')
                i = 1
                while i < size-1:
                    self.fill_empty(row+i, col, 'm')
                    i+=1
                self.fill_empty(row+size-1, col, 'b')

        self.placed[size-1] -= 1

        self.water_around_boat(row, col, size, direction)
    

    def get_hints(self):
        return self.hints


    def fits_boat(self,size):
        counter = 0  
        lista_posi = []

        if size == 1:
            fits_rows = np.where(self.get_rows() >= size)
            for row in fits_rows[0]:
                empty = np.where(self.board[row] == ' ')
                for col in empty[0]:
                    lista_posi.append([row, col, 1, size])
        else:
            fits_cols = np.where(self.get_columns() >= size)  
            for i in fits_cols[0]:
                empty = np.where(self.board[:, i] == ' ')
                for j in empty[0]:
                    counter = 0
                    l = j
                    while l < 10:
                        slot = self.get_value(l,i)
                        if counter < size:
                            if (slot == ' '):
                                counter += 1
                                l+=1
                            else: break
                        if (counter == size):
                            lista_posi.append([j , i, 1, size])
                            break
            fits_rows = np.where(self.get_rows() >= size)
            for i in fits_rows[0]:
                empty = np.where(self.board[i] == ' ')
                for j in empty[0]:
                    counter = 0
                    l = j
                    while l < 10:
                        slot = self.get_value(i,l)
                        if counter < size:
                            if (slot == ' '):
                                counter += 1
                                l+=1
                            else: break
                        if (counter == size):
                            lista_posi.append([i , j, 0, size])
                            break
        return lista_posi


    def verify_free_slots(self):
        rows = np.where(self.get_rows() > 0)
        cols = np.where(self.get_columns() > 0)

        for r in rows[0]:
            empty = np.where(self.board[r] == ' ')
            if np.size(empty[0]) < self.get_rows()[r]: return False

        for c in cols[0]: 
            empty = np.where(self.board[:, c] == ' ')
            if np.size(empty[0]) < self.get_columns()[c]: return False

        return True


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        state_board = state.get_state_board()

        if not state_board.verify_free_slots(): 
            return []
        
        placed = state_board.get_placed()

        if placed[3] != 0:
            list_posi = state_board.fits_boat(4)
            size = 4
        elif placed[2] != 0:
            list_posi = state_board.fits_boat(3)
            size = 3
        elif placed[1] != 0:
            list_posi = state_board.fits_boat(2)
            size = 2
        elif placed[0] != 0:
            list_posi = state_board.fits_boat(1)
            size = 1

        else: return []
        return list_posi


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
        rows = np.where(state_board.get_rows() == 0)
        cols = np.where(state_board.get_columns() == 0)
        hints = state_board.get_hints()
        placed = state_board.get_placed()
        used = np.where(placed == 0)
        
        if not state_board.verify_free_slots(): return False

        for i in hints:
            if state_board.get_value(int(i[0]), int(i[1])) != i[2].lower():
                return False
        
        if np.size(used[0]) != 4:   
            return False

        if np.size(rows[0]) != 10: return False
        if np.size(cols[0]) != 10: return False
        
        for i in hints:
            state_board.replace_piece(int(i[0]), int(i[1]), i[2])
        
        return True


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass


if __name__ == "__main__":

    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    board = Board.parse_instance()
    problem = Bimaru(board)
    goal_node = depth_first_tree_search(problem)
   
    print(goal_node.state.get_state_board(), end = '')