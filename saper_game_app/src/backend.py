class GameOverError(Exception):
    pass


class Plansza():
    mine_mark = 9

    def __init__(self, num_of_rows, num_of_columns):
        self._row_lenght = num_of_columns
        self._column_length = num_of_rows
        self._board = []
        for i in range(num_of_rows):
            self._board.append([])
        for row in self._board:
            for i in range(num_of_columns):
                row.append(0)

    def get_value(self, i, j):
        return self._board[i][j]

    def place_mines(self, list_of_coordinates):
        for i, j in list_of_coordinates:
            self.place_mine(i, j)
        self._fill_board_with_adjacent_mines_numbers()

    
    def place_mine(self, i, j):
        self._board[i][j] = self.mine_mark
        

    def _fill_board_with_adjacent_mines_numbers(self):
        # ???????
        for row_idx in range(self._column_length):
            for colum_idx in range(self._row_lenght):
                if self._board[row_idx][colum_idx] == self.mine_mark:
                    self._add_one_to_all_adjacent_fieds(row_idx, colum_idx)

    def _add_one_to_all_adjacent_fieds(self, row_idx, colum_idx):
        # Increase upper row
        modificators = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for mod_x, mod_y in modificators:
            try:
                if self._board[row_idx + mod_x][colum_idx + mod_y] != self.mine_mark:
                    self._board[row_idx + mod_x][colum_idx + mod_y] += 1
            except IndexError:
                pass

    def __str__(self):
        ret_str = ''
        for row in self._board:
            ret_str += str(row) + '\n'
        return ret_str


class ButtonsMap():

    def __init__(self, num_of_rows, num_of_columns):
        self._row_lenght = num_of_columns
        self._column_length = num_of_rows
        self._board = []
        for i in range(num_of_rows):
            self._board.append([])
        for row in self._board:
            for i in range(num_of_columns):
                row.append('e')

    def set_value(self, i, j, value):
        self._board[i][j] = value

    def get_value(self, i, j):
        return self._board[i][j]

    def __str__(self):
        ret_str = '  0 1 2 3 4 5 6 7\n'
        for row_number, row in enumerate(self._board):
            ret_str += str(row_number) + ' '
            for entry in row:
                ret_str += str(entry) + ' '
            ret_str += '\n'
        return ret_str


class SaperGame():

    def __init__(self):
        self.board = Plansza(8, 8)
        self.board_state = ButtonsMap(8, 8)
        self._insert_number_of_mines(10)

    def _insert_number_of_mines(self, number):
        lisa_min = [
            (1, 2),
            (7, 4),
            (1, 2),
            (3, 2),
            (7, 7),
            (6, 1),
            (6, 7),
            (6, 3),
            (4, 6),
            (6, 1),
        ]
        self.board.place_mines(lisa_min)

    def game_state(self):
        return str(self.board_state)

    def _reveal_adjacent_fields(self, i, j):
        modificators = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]
        for mod_x, mod_y in modificators:
            if i + mod_x >= 0 and j + mod_y >= 0:
                try:
                    if self.board_state.get_value(i + mod_x, j + mod_y) == 'e':
                        value = self.board.get_value(i + mod_x, j + mod_y)
                        self.board_state.set_value(i + mod_x, j + mod_y, value)
                        if value == 0:
                            self._reveal_adjacent_fields(i + mod_x, j + mod_y)
                except IndexError:
                    pass

        

    def take_player_input(self, i, j):
        value = self.board.get_value(i, j)
        self.board_state.set_value(i, j, value)
        if value == 9:
            raise GameOverError()
        if value == 0:
            self._reveal_adjacent_fields(i, j)

if __name__ == '__main__':
    g = SaperGame()
    print(g.game_state())
    while True:
        coords = input('Podaj wspolrzedne')
        temp = coords.split()
        i = int(temp[0])
        j = int(temp[1])
        g.take_player_input(i, j)
        print(g.game_state())

