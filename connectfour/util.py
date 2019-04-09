"""
Module to utility functionality to aid students in building
Connect Four playing agents.
"""

import time


def manhattan_distance(start, end):
    sx, sy = start
    ex, ey = end
    return abs(ex - sx) + abs(ey - sy)


def player_token_locations(board, player):
    """
    A generator of cell locations where the specified player has a token.
    """
    for row in range(board.height):
        for col in range(board.width):
            if board.get_cell_value(row, col) == player.id:
                yield (row, col)


def delay_move_execution(move_fn):
    """
    A decorator function that will ensure the wrapped move function
    takes *at least* a set amount of time to execute. Used to impose
    a minimum execution time on a computer player move, which acts as a
    delay on move speed.

    Args:
        move_fn: The function which executes a computer move. Takes no arguments.
    """
    max_execution_time_in_sec = 1

    def wrapper():
        start = time.time()
        move = move_fn()
        end = time.time()
        execution_time = end - start
        end_delay = max(max_execution_time_in_sec - execution_time, 0)
        time.sleep(end_delay)
        return move
    return wrapper
