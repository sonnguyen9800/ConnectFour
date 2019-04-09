from connectfour.board import Board


class TestBoard:
    def test_try_move_on_valid_column(self):
        board = Board()

        for i in range(board.width):
            col = board.try_move(i)
            # expected position is bottom of board
            assert col == board.height - 1

    def test_try_move_on_invalid_column(self):
        board = Board()
        column_to_fill = 1

        for i in range(board.height):
            board.board[i][column_to_fill] = 1

        # Placement in column should now fail
        assert board.try_move(column_to_fill) == -1
        # Other columns should still be valid
        assert board.try_move(column_to_fill + 1) >= 0

    def test_valid_move_on_valid_move(self):
        board = Board()

        col = 2
        # at start, a peice should be placed on the bottom
        assert board.valid_move(board.height - 1, col)
        assert not board.valid_move(board.height - 2, col)

    def test_terminal_on_finished_game(self):
        board = Board()

        # A connect four game is considered finished when all columns
        # are full. In the Board class, this is indicated by non-zero values
        # in the first row
        for i in range(board.width):
            board.board[0][i] = 1
        assert board.terminal()

    def test_terminal_on_unfinished_game(self):
        board = Board()
        assert not board.terminal()

        board.board[1][1] = 1
        assert not board.terminal()

    def test_legal_moves(self):
        board = Board()

        # fill rows 0, 3, and 5
        for i in range(board.height):
            board.board[i][0] = board.board[i][3] = board.board[i][5] = 1

        legal_columns = board.legal_moves()

        expected = [1, 2, 4, 6]
        for i, col in enumerate(legal_columns):
            assert expected[i] == col

    def test_winner(self):
        column_cases = [
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, -1],
                    [0, 0, 0, 0, 0, 0, -1],
                    [0, 0, 0, 0, 0, 0, -1],
                    [1, 1, 1, 0, 0, 0, -1],
                ],
                -1,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, -1],
                    [0, 0, 0, 0, 0, 0, -1],
                    [0, 0, 0, 0, 0, 0, -1],
                    [0, 0, 0, 0, 0, 0, -1],
                    [0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 1, -1, 1, 1],
                ],
                -1,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, -1],
                    [0, 0, 1, 0, 0, 0, -1],
                    [1, 1, 1, -1, 0, 0, -1],
                ],
                1,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1],
                    [0, 0, -1, 0, 0, 0, 1],
                    [0, 0, 1, 0, 0, 0, 1],
                    [0, -1, 1, -1, 0, 0, -1],
                    [1, 1, 1, -1, -1, 0, -1],
                ],
                1,
            ),
        ]

        for case in column_cases:
            board = Board(case[0])
            assert case[1] == board.winner()

        row_cases = [
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, -1, 0, 0, 0, 0, 0],
                    [-1, -1, 0, 0, 0, 0, 0],
                    [1, -1, 1, 1, 1, 1, 0],
                ],
                1,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [-1, -1, -1, -1, 0, 0, 0],
                    [1, 1, 1, -1, 1, 1, 0],
                ],
                -1,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 0, 0, 0],
                    [1, 0, 1, 0, 0, 0, 0],
                    [1, -1, -1, -1, -1, 0, 0],
                    [-1, 1, -1, 1, -1, 1, -1],
                    [1, -1, 1, -1, 1, -1, 1],
                ],
                -1,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [-1, -1, 0, 0, 0, 0, 1, 1, 1, 1],
                ],
                1,
            ),
        ]

        for case in row_cases:
            board = Board(case[0])
            assert case[1] == board.winner()

        diag_cases = [
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, -1, -1, 0],
                    [0, 0, 1, -1, -1, 1, 0],
                    [0, 0, -1, -1, 1, -1, 0],
                    [0, -1, 1, 1, 1, -1, 0],
                ],
                -1,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0],
                    [-1, 1, 1, 0, -1, -1, 0],
                    [1, -1, 1, -1, -1, 1, 0],
                    [1, 1, -1, -1, 1, -1, 0],
                    [1, -1, 1, -1, 1, -1, 0],
                ],
                -1,
            ),
            (
                [
                    [0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 0],
                    [0, 0, 0, -1, -1, 1, 0],
                    [0, 0, 0, 1, 1, -1, 1],
                    [0, 0, 0, -1, 1, 1, 1],
                    [0, 0, 0, 1, -1, -1, -1],
                ],
                1,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [1, 0, 1, -1, -1, 0, 0],
                    [1, 1, -1, 1, 1, 0, 0],
                    [-1, 1, 1, 1, -1, 0, 0],
                    [-1, 1, -1, 1, -1, -1, 0],
                ],
                1,
            ),
        ]

        for case in diag_cases:
            board = Board(case[0])
            assert case[1] == board.winner()

    def test_winner_on_connect_three(self):
        cases = [
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, -1],
                    [0, 0, 0, 0, 0, 0, -1],
                    [1, 1, 0, 0, 0, 0, -1],
                ],
                -1,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1],
                    [0, -1, 0, 0, 0, 0, -1],
                    [1, 1, 1, 0, 0, 0, -1],
                ],
                1,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, -1],
                    [1, 1, 0, 0, 0, 0, -1],
                ],
                0,
            ),
            (
                [
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 1],
                    [0, 1, -1, 0, 0, 0, -1],
                    [1, 1, -1, 0, 0, -1, -1],
                ],
                1,
            ),
        ]

        for case in cases:
            board = Board(case[0], num_to_connect=3)
            assert case[1] == board.winner()

    def test__build_winning_zones_map(self):
        board = Board()

        zones_map = board._build_winning_zones_map()
        default_seven_by_size_zones_map = [
            [
                [0, 24, 45],
                [4, 24, 25, 49],
                [8, 24, 25, 26, 53],
                [12, 24, 25, 26, 60],
                [16, 25, 26, 64],
                [20, 26, 68],
            ],
            [
                [0, 1, 27, 46],
                [4, 5, 27, 28, 45, 50],
                [8, 9, 27, 28, 29, 49, 54, 60],
                [12, 13, 27, 28, 29, 53, 59, 64],
                [16, 17, 28, 29, 63, 68],
                [20, 21, 29, 67],
            ],
            [
                [0, 1, 2, 30, 47],
                [4, 5, 6, 30, 31, 46, 51, 60],
                [8, 9, 10, 30, 31, 32, 45, 50, 55, 59, 64],
                [12, 13, 14, 30, 31, 32, 49, 54, 58, 63, 68],
                [16, 17, 18, 31, 32, 53, 62, 67],
                [20, 21, 22, 32, 66],
            ],
            [
                [0, 1, 2, 3, 33, 48, 60],
                [4, 5, 6, 7, 33, 34, 47, 52, 59, 64],
                [8, 9, 10, 11, 33, 34, 35, 46, 51, 56, 58, 63, 68],
                [12, 13, 14, 15, 33, 34, 35, 45, 50, 55, 57, 62, 67],
                [16, 17, 18, 19, 34, 35, 49, 54, 61, 66],
                [20, 21, 22, 23, 35, 53, 65],
            ],
            [
                [1, 2, 3, 36, 59],
                [5, 6, 7, 36, 37, 48, 58, 63],
                [9, 10, 11, 36, 37, 38, 47, 52, 57, 62, 67],
                [13, 14, 15, 36, 37, 38, 46, 51, 56, 61, 66],
                [17, 18, 19, 37, 38, 50, 55, 65],
                [21, 22, 23, 38, 54],
            ],
            [
                [2, 3, 39, 58],
                [6, 7, 39, 40, 57, 62],
                [10, 11, 39, 40, 41, 48, 61, 66],
                [14, 15, 39, 40, 41, 47, 52, 65],
                [18, 19, 40, 41, 51, 56],
                [22, 23, 41, 55],
            ],
            [
                [3, 42, 57],
                [7, 42, 43, 61],
                [11, 42, 43, 44, 65],
                [15, 42, 43, 44, 48],
                [19, 43, 44, 52],
                [23, 44, 56],
            ],
        ]
        assert zones_map == default_seven_by_size_zones_map

    def test__num_of_winning_zones(self):
        board = Board()
        expected = 69
        assert expected == board._num_of_winning_zones(num_to_connect=4)
