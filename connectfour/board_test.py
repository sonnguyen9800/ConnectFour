from connectfour.board import Board
import numpy as np

board = Board()

board = board.next_state(2, 0)
board = board.next_state(2, 1)
board = board.next_state(2, 2)
board = board.next_state(2, 3)


#print(board._build_winning_zones_map())
print(board._check_rows())