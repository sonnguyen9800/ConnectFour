import copy
import random

dx = [1, 1, 1, 0]
dy = [1, 0, -1, 1]


class Board(object):
    DEFAULT_WIDTH = 7
    DEFAULT_HEIGHT = 6
    all_moves = []

    def __init__(
        self,
        board=None,
        height=None,
        width=None,
        last_move=[None, None],
        #all_moves=None,
        num_to_connect=4
    ):
        if board is not None and (height is not None or width is not None):
            raise RuntimeError('Cannot specify both a board and a board size value')

        self.board = board if board is not None else self._empty_board(height, width)
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.last_move = last_move
        #self.all_moves = all_moves
        #self.all_moves.append(last_move)
        self.num_to_connect = num_to_connect
        self.winning_zones = self._build_winning_zones_map()
        self.score_array = [
            [0] * self._num_of_winning_zones(num_to_connect),
            [0] * self._num_of_winning_zones(num_to_connect)
        ]
        self.current_player_score = [0, 0]

    def get_cell_value(self, row, col):
        """
        Access the board's underlying cell array and retreive the value
        at a specific (row, col) location.
        1 -> Player One token
        2 -> Player Two token
        0 -> Empty
        """
        if row >= self.height or col >= self.width:
            raise ValueError('({}, {}) is an invalid location on the board')

        return self.board[row][col]

    def try_move(self, move):
        """
        Takes the current board and a possible move specified
        by the column. Returns the appropiate row where the
        piece will be located. If it's not found it returns -1.
        """
        if move < 0 or move >= self.width or self.board[0][move] != 0:
            return -1

        for i in range(len(self.board)):
            if self.board[i][move] != 0:
                return i - 1
        return len(self.board) - 1

    def valid_move(self, row, col):
        """
        Take a row, col position on the board and returns whether
        that row value is the bottom-most empty position in the column.

        Args:
            row: int value for row position on Board
            col: int value for column position on Board

        Returns: True is move is valid. False, otherwise
        """
        return row >= 0 and self.try_move(col) == row

    def valid_moves(self):
        """
        Returns: A generator of all valid moves in the current board state
        """
        for col in range(self.width):
            for row in range(self.height):
                if self.valid_move(row, col):
                    yield (row, col)

    def terminal(self):
        """
        Returns true when the game is finished, otherwise false.
        """
        # check for a winner:
        if (self.winner() == 0):
            return False

        for i in range(len(self.board[0])):
            if self.board[0][i] == 0:
                return False
        return True

    def legal_moves(self):
        """
        Returns the full list of legal moves that for next player.
        """
        legal = []
        for i in range(len(self.board[0])):
            if self.board[0][i] == 0:
                legal.append(i)

        return legal

    def next_state_rand(self, turn):
        aux = copy.deepcopy(self)
        moves = aux.legal_moves()
        if len(moves) > 0:
            ind = random.randint(0, len(moves) - 1)
            row = aux.try_move(moves[ind])
            aux.board[row][moves[ind]] = turn
            aux.last_move = [row, moves[ind]]
        return aux

    def next_state(self, turn, col):
        next_board = copy.deepcopy(self)
        moves = next_board.legal_moves()

        if(col not in moves):
            return 0

        row = next_board.try_move(col)
        next_board.board[row][col] = turn
        next_board.last_move = [row, col]
        return next_board

    def _empty_board(self, height, width):
        if height is None:
            height = self.DEFAULT_HEIGHT
        if width is None:
            width = self.DEFAULT_WIDTH

        if height <= 0 or width <= 0:
            raise ValueError('height or width of board cannot be less than 1')

        board = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(0)
            board.append(row)
        return board

    def winner(self):
        """
        Takes the board as input and determines if there is a winner.
        If the game has a winner, it returns the player number (Player One = 1, Player Two = 2).
        If the game is still ongoing, it returns zero.
        """
        row_winner = self._check_rows()
        if row_winner:
            return row_winner
        col_winner = self._check_columns()
        #print("col winner = ", col_winner)
        if col_winner:
            return col_winner
        diag_winner = self._check_diagonals()
        if diag_winner:
            return diag_winner
        return 0  # no winner yet

    def _check_rows(self):
        for row in self.board:
            same_count = 1
            curr = row[0]
            for i in range(1, self.width):
                if row[i] == curr:
                    same_count += 1
                    if same_count == self.num_to_connect and curr != 0:
                        return curr
                else:
                    same_count = 1
                    curr = row[i]
        return 0

    def _check_columns(self):
        for i in range(self.width):
            same_count = 1
            curr = self.board[0][i]
            for j in range(1, self.height):
                if self.board[j][i] == curr:
                    same_count += 1
                    if same_count == self.num_to_connect and curr != 0:
                        return curr
                else:
                    same_count = 1
                    curr = self.board[j][i]
        return 0

    def _check_diagonals(self):
        boards = [
            self.board,
            [row[::-1] for row in copy.deepcopy(self.board)]
        ]

        for b in boards:
            for i in range(self.width - self.num_to_connect + 1):
                for j in range(self.height - self.num_to_connect + 1):
                    if i > 0 and j > 0:  # would be a redundant diagonal
                        continue

                    # (j, i) is start of diagonal
                    same_count = 1
                    curr = b[j][i]
                    k, m = j + 1, i + 1
                    while k < self.height and m < self.width:
                            if b[k][m] == curr:
                                same_count += 1
                                if same_count is self.num_to_connect and curr != 0:
                                    return curr
                            else:
                                same_count = 1
                                curr = b[k][m]
                            k += 1
                            m += 1
        return 0

    def update_scores(self, x, y, current_player, is_player_one):
        this_difference = 0
        other_difference = 0
        current_score_array = self.score_array
        if is_player_one:
            player = 0
            other_player = 1
        else:
            player = 1
            other_player = 0

        # agent = current_state->agents[(depth % 2 == 1) ? player : other(player)];
        # double score;

        # Update line-scores
        for i in range(len(self.winning_zones[x][y])):
            win_index = self.winning_zones[x][y][i]
            this_difference += current_score_array[player][win_index]
            other_difference += current_score_array[other_player][win_index]
            current_score_array[player][win_index] += 1

        # TODO: Don't think we need this
        # if (agent != NULL)
        # {
        #    score = agent->agentFunction(current_state, player, x, y);
        #
        #    current_state->score[player] = score;
        #    current_state->score[other_player] = 0;
        # }

    def _build_winning_zones_map(self):
        size_y = self.height
        size_x = self.width
        i = j = k = win_index = 0
        map_ = []
        num_to_connect = self.num_to_connect

        # initialise the zones maps
        for i in range(size_x):
            map_.append([])
            for j in range(size_y):
                map_[i].append([])

        # Fill in the horizontal win positions
        for i in range(size_y):
            for j in range(size_x-num_to_connect+1):
                for k in range(num_to_connect):
                    win_indices = map_[j+k][i]
                    win_indices.append(win_index)
                win_index += 1

        # Fill in the vertical win positions
        for i in range(size_x):
            for j in range(size_y-num_to_connect+1):
                for k in range(num_to_connect):
                    win_indices = map_[i][j+k]
                    win_indices.append(win_index)
                win_index += 1

        # Fill in the forward diagonal win positions
        for i in range(size_y - num_to_connect + 1):
            for j in range(size_x-num_to_connect+1):
                for k in range(num_to_connect):
                    win_indices = map_[j+k][i+k]
                    win_indices.append(win_index)
                win_index += 1

        # Fill in the backward diagonal win positions
        for i in range(size_y - num_to_connect + 1):
            for j in range(size_x - 1, num_to_connect - 1 - 1, -1):
                for k in range(num_to_connect):
                    win_indices = map_[j-k][i+k]
                    win_indices.append(win_index)
                win_index += 1

        return map_

    def _num_of_winning_zones(self, num_to_connect=4):
        if self.width < num_to_connect and self.height < num_to_connect:
            return 0
        elif self.width < num_to_connect:
            return self.width * ((self.height - num_to_connect) + 1)
        elif self.height < num_to_connect:
            return self.height * ((self.width - num_to_connect) + 1)
        else:
            return (
                4 * self.width * self.height -
                3 * self.width * num_to_connect -
                3 * self.height * num_to_connect +
                3 * self.width + 3 * self.height -
                4 * num_to_connect +
                2 * num_to_connect * num_to_connect + 2
            )
