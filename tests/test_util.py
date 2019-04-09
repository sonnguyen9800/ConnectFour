from connectfour import util
from connectfour.board import Board


def test_manhattan_distance():
    assert 0 == util.manhattan_distance((0, 0), (0, 0))
    assert 1 == util.manhattan_distance((0, 0), (0, 1))
    assert 1 == util.manhattan_distance((0, 0), (1, 0))
    assert 4 == util.manhattan_distance((0, 0), (2, 2))


class MockPlayer:
    def __init__(self, id):
        self.id = id


def test_player_token_locations():
    player_id = "hello"
    player = MockPlayer(player_id)
    board = Board()

    board.board[1][1] = player_id
    board.board[2][1] = player_id
    board.board[2][2] = "not player id"
    board.board[2][4] = player_id
    board.board[5][5] = player_id

    expected = [(1, 1), (2, 1), (2, 4), (5, 5)]

    assert expected == list(util.player_token_locations(board, player))
