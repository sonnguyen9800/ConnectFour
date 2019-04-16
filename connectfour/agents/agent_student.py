import copy
import math

from connectfour.agents.computer_player import RandomAgent


def close_to_win(board, id):
    score = 0
    board_cp = copy.deepcopy(board)
    for i in range(board_cp.width):
        if board_cp.try_move(i) == -1:
            continue
        sub_board = board_cp.next_state(id, i)
        if sub_board.winner() == id:
            score += 1
    if score >= 2:
        return 2
    if score == 1:
        return 1
    return 0


def get_correct_segment_dia(board, id):
    all_dia_correct_segment = []
    # For the dash //

    for row in range(board.num_to_connect - 1, board.height):
        for col in range(board.width - 3):

            flag = True
            sub_row = 0
            sub_col = 0
            for i in range(board.num_to_connect):

                if board.get_cell_value(row + sub_row, col + sub_col) != id:
                    flag = False
                    break
                sub_row -= 1
                sub_col += 1

            sub_row = 0
            sub_col = 0
            if flag:
                dia_segment = Segment()
                for i in range(board.num_to_connect):
                    dia_segment.add_pos([row + sub_row, col + sub_col])
                    sub_row -= 1
                    sub_col += 1
                all_dia_correct_segment.append(dia_segment)

    for row in range(board.height - board.num_to_connect + 1):
        for col in range(board.width - board.num_to_connect + 1):

            flag = True

            sub = 0
            for i in range(board.num_to_connect):

                if board.get_cell_value(row + sub, col + sub) != id:
                    flag = False
                    break
                sub += 1

            sub = 0
            if flag:
                dia_segment = Segment()
                for i in range(board.num_to_connect):
                    dia_segment.add_pos([row + sub, col + sub])
                    sub += 1
                all_dia_correct_segment.append(dia_segment)

    return all_dia_correct_segment


def get_correct_segment_col(board, id):
    all_col_segment = []

    for col in range(0, board.width):

        for row in range(0, board.height - board.num_to_connect + 1):

            flag = True
            # Check from [row, col] to [row+3, col] and see if they make a correct segment
            for i in range(row, row + board.num_to_connect):
                if board.get_cell_value(i, col) != id:
                    flag = False
                    break

            # If they did make a correct segment- create a Segment Object and input the position of correct node
            if flag:
                col_segment = Segment()
                for i in range(row, row + board.num_to_connect):
                    col_segment.add_pos([i, col])
                all_col_segment.append(col_segment)

    return all_col_segment


def get_correct_segment_row(board, id):
    all_row_segment = []
    # print(np.matrix(board.board))
    for row in range(0, board.height):

        for col in range(0, board.width - board.num_to_connect + 1):

            flag = True
            # Check from [row, col] to [row, col+3] and see if they make a correct segment
            for i in range(col, col + board.num_to_connect):
                if board.get_cell_value(row, i) != id:
                    flag = False
                    break

            # If they did make a correct segment- create a Segment Object and input the position of correct node
            if flag:
                row_segment = Segment()
                for i in range(col, col + board.num_to_connect):
                    row_segment.add_pos([row, i])
                all_row_segment.append(row_segment)

    return all_row_segment


def fill_all_pos(board, id):
    # DONE
    board_copy = copy.deepcopy(board)
    for row in range(board.height):
        for col in range(board.width):
            if board_copy.get_cell_value(row, col) == 0:
                board_copy.board[row][col] = id

    return board_copy


def marked_token(board, id):
    array = []
    # Return : a list of location (row,list) - they are all location of token that are marked
    for row in range(board.height):
        for col in range(board.width):
            if board.get_cell_value(row, col) == id:
                array.append([row, col])
    return array


class StudentAgent(RandomAgent):
    main_board = 1

    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 4

    def get_move(self, board):

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id, move[1])
            moves.append(move)
            vals.append(self.dfMiniMax(next_state, 1))

        bestMove = moves[vals.index(max(vals))]

        return bestMove

    def dfMiniMax(self, board, depth):

        if depth == self.MaxDepth:
            return self.evaluateBoardState(board)

        valid_moves = board.valid_moves()
        vals = []
        moves = []

        for move in valid_moves:
            if depth % 2 == 1:
                next_state = board.next_state(self.id % 2 + 1, move[1])
            else:
                next_state = board.next_state(self.id, move[1])

            moves.append(move)
            vals.append(self.dfMiniMax(next_state, depth + 1))

        if depth % 2 == 1:
            bestVal = min(vals)
        else:
            bestVal = max(vals)

        return bestVal  #

    def evaluateBoardState(self, board):
        flag = False
        extreme_check = 0
        if board.winner() == self.id:
            # print("YOU WIN")
            return math.inf
        elif board.winner() == (self.id % 2 + 1):
            # print("You Lose")
            return -math.inf

        step_to_win_allies = close_to_win(board, self.id)
        step_to_win_enemy = close_to_win(board, self.id % 2 + 1)

        # Death_thread: lose 100%
        if step_to_win_enemy >= 2:
            extreme_check = -100000
        # Enemy need one more turn to win and also  it is his/her turn
        if step_to_win_enemy == 1 and (self.what_turn(board) != self.id):
            extreme_check = -100000
        # Our team has one more turn to win and also now it is our turn
        if step_to_win_allies >= 1 and (self.what_turn(board) == self.id):
            extreme_check = 100000

        old_post_array_our = marked_token(board, self.id)
        old_post_array_enemy = marked_token(board, self.id % 2 + 1)

        correct_segment = self.get_all_correct_segments(board, self.id)
        correct_segment_enemy = self.get_all_correct_segments(board, self.id % 2 + 1)

        n1 = 0
        for i in correct_segment:
            if i.count_old_pos(old_post_array_our) == 1:
                n1 += 1

        n2 = 0
        for i in correct_segment:
            if i.count_old_pos(old_post_array_our) == 2:
                n2 += 1

        n3 = 0
        for i in correct_segment:
            if i.count_old_pos(old_post_array_our) == 3:
                n3 += 1

        n4 = 0
        for i in correct_segment:
            if i.count_old_pos(old_post_array_our) == 4:
                n4 += 1
        n1_enemy = 0
        for i in correct_segment_enemy:
            if i.count_old_pos(old_post_array_enemy) == 1:
                n1_enemy += 1

        n2_enemy = 0
        for i in correct_segment_enemy:
            if i.count_old_pos(old_post_array_enemy) == 2:
                n2_enemy += 1

        n3_enemy = 0
        for i in correct_segment_enemy:
            if i.count_old_pos(old_post_array_enemy) == 3:
                n3_enemy += 1

        n4_enemy = 0
        for i in correct_segment_enemy:
            if i.count_old_pos(old_post_array_enemy) == 4:
                n4_enemy += 1

        if flag:
            print("N1 : {} ; N2 : {} ; N3 {} ; N4 {}:".format(n1, n2, n3, n4))
            print("Evaluate: {}".format(self.evaluate(n3, n2, n1)))
            print("Enemy: N1 : {} ; N2 : {} ; N3 {} ; N4 {}:".format(n1_enemy, n2_enemy, n3_enemy, n4_enemy))
            print("Evaluate: {}".format(self.evaluate(n3_enemy, n2_enemy, n1_enemy)))
            print("Extreme Check: {}".format(extreme_check))
            print("Need {} steps to win".format(step_to_win_allies))
            print("Need {} steps to lose".format(step_to_win_enemy))
            print("Current Turn belong to player {}".format(self.what_turn(board)))

        return self.evaluate(n3, n2, n1) \
               - self.evaluate(n3_enemy, n2_enemy, n1_enemy) \
               + extreme_check

    @staticmethod
    def get_all_correct_segments(board, id):

        # 1. filling the board_copy with self.token - create object broad_copy - DONE
        board_copy = fill_all_pos(board, id)

        # 2. Making a list of correct segment
        correct_segment = []

        correct_segment_row = get_correct_segment_row(board_copy, id)
        correct_segment_col = get_correct_segment_col(board_copy, id)
        correct_segment_dia = get_correct_segment_dia(board_copy, id)
        # print("Get all Segment Row: {}".format(len(correct_segment_row)))

        for i in correct_segment_row:
            correct_segment.append(i)
        for i in correct_segment_col:
            correct_segment.append(i)
        for i in correct_segment_dia:
            correct_segment.append(i)
        return correct_segment

    @staticmethod
    def evaluate(num_opening_three, num_opening_two, num_opening_one):
        return 1 * num_opening_one + 10 * num_opening_two + 100 * num_opening_three

    @staticmethod
    def what_turn(board):
        count_turn_num_1 = 0
        count_turn_num_2 = 0
        token1 = 0
        token2 = 0

        # find for token 1
        for row in range(board.height):
            flag = False
            for col in range(board.width):
                if board.get_cell_value(row, col) != 0:
                    token1 = board.get_cell_value(row, col)
                    flag = True
                    break
            if flag:
                break
            else:
                continue
        # find for token 2
        for row in range(board.height):
            flag = False
            for col in range(board.width):
                if board.get_cell_value(row, col) != 0 and board.get_cell_value(row, col) != token1:
                    token2 = board.get_cell_value(row, col)
                    flag = True
                    break
            if flag:
                break
            else:
                continue

        for row in range(board.height):
            for col in range(board.width):
                if board.get_cell_value(row, col) == token1:
                    count_turn_num_1 += 1
                if board.get_cell_value(row, col) == token2:
                    count_turn_num_2 += 1
        #
        # print("Player {} moved {} turn".format(token1, count_turn_num_1))
        # print("Player {} moved {} turn".format(token2, count_turn_num_2))

        if count_turn_num_1 == count_turn_num_2:
            return token1
        else:
            return token2


class Segment:
    position_array = []

    def __init__(self):
        self.position_array = []

    def add_pos(self, element):
        self.position_array.append(element)

    def __str__(self):
        return self.position_array

    def get_size(self):
        return self.position_array.__sizeof__()

    def count_old_pos(self, array):
        count = 0
        for element in self.position_array:
            if element in array:
                count += 1
        return count
