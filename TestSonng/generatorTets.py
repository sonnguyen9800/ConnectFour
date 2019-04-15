def valid_move(n):
    if n % 2 == 0:
        return True
    else:
        return False

def valid_moves(n):
    """
    Returns: A generator of all valid moves in the current board state
    """
    for i in range(n):
        if valid_move(i):
            yield i

x = valid_moves(15);
for i in x:
    print(i)