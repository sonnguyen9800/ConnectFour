import numpy as np

from connectfour.agents.computer_player import RandomAgent
import copy
import logging


class StudentAgent(RandomAgent):
    main_board = 1

    def __init__(self, name):
        super().__init__(name)
        self.MaxDepth = 2

    def get_move(self, board):
        logging.info("get_move")
        valid_moves = board.valid_moves()  # Get the valid moves from the board
        logging.info("get_valid_moves")
        vals = []
        moves = []

        for move in valid_moves:
            next_state = board.next_state(self.id,
                                          move[1])  # Create the next state: next_state take: id (first parameter) &
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

        old_post_array = self.marked_token(board)

        correct_segment = self.get_all_correct_segments(board)
        #print("Size Correct Segment {}".format(len(correct_segment)))
        n1 = 0
        for i in correct_segment:
            if i.count_old_pos(old_post_array) == 1:
                n1 += 1
        #print("N1: {}".format(n1))
        n2 = 0
        for i in correct_segment:
            if i.count_old_pos(old_post_array) == 2:
                n2 += 1
        #print("N2: {}".format(n2))
        n3 = 0
        for i in correct_segment:
            if i.count_old_pos(old_post_array) == 3:
                n3 += 1
        #print("N3: {}".format(n3))
        n4 = 0
        for i in correct_segment:
            if i.count_old_pos(old_post_array) == 4:
                n4 += 1
        #print("N4: {}".format(n4))
        return self.evaluate(n4, n3, n2, n1)

    def marked_token(self, board):
        array = []
        # Return : a list of location (row,list) - they are all location of token that are marked
        for row in range(board.height):
            for col in range(board.width):
                if board.get_cell_value(row, col) == self.id:
                    array.append([row, col])
        return array

    def fill_all_pos(self, board):
        #DONE
        board_copy = copy.deepcopy(board)
        for row in range(board.height):
            for col in range(board.width):
                if board_copy.get_cell_value(row, col) == 0:
                    board_copy.board[row][col] = self.id

        return board_copy

    def get_all_correct_segments(self, board):

        # 1. filling the board_copy with self.token - create object broad_copy - DONE
        board_copy = self.fill_all_pos(board)

        # 2. Making a list of correct segment
        correct_segment = []

        correct_segment_row = self.get_correct_segment_row(board_copy)
        correct_segment_col = self.get_correct_segment_col(board_copy)
        correct_segment_dia = self.get_correct_segment_dia(board_copy)
        #print("Get all Segment Row: {}".format(len(correct_segment_row)))

        for i in correct_segment_row:
            correct_segment.append(i)
        for i in correct_segment_col:
            correct_segment.append(i)
        for i in correct_segment_dia:
            correct_segment.append(i)
        return correct_segment

    @staticmethod
    def evaluate(num_four, num_opening_three, num_opening_two, num_opening_one):
        return 1 * num_opening_one + 10 * num_opening_two + 100 * num_opening_three + 10000 * num_four

    def get_correct_segment_row(self, board):
        all_row_segment = []
        #print(np.matrix(board.board))
        for row in range(0, board.height):

            for col in range(0, board.width - board.num_to_connect + 1):

                flag = True
                #Check from [row, col] to [row, col+3] and see if they make a correct segment
                for i in range(col, col + board.num_to_connect):
                    if board.get_cell_value(row, i) != self.id:
                        flag = False
                        break

                #If they did make a correct segment- create a Segment Object and input the position of correct node
                if flag == True:
                    row_segment = Segment()
                    for i in range(col, col + board.num_to_connect):
                        row_segment.add_pos([row, i])
                    all_row_segment.append(row_segment)


        return all_row_segment

    def get_correct_segment_col(self, board):
        all_col_segment = []

        for col in range(0, board.width):

            for row in range(0, board.height - board.num_to_connect + 1):

                flag = True
                # Check from [row, col] to [row+3, col] and see if they make a correct segment
                for i in range(row, row + board.num_to_connect):
                    if board.get_cell_value(i, col) != self.id:
                        flag = False
                        break

                # If they did make a correct segment- create a Segment Object and input the position of correct node
                if flag == True:
                    col_segment = Segment()
                    for i in range(row, row + board.num_to_connect):
                        col_segment.add_pos([i, col])
                    all_col_segment.append(col_segment)

        return all_col_segment

    def get_correct_segment_dia(self, board):

        all_dia_correct_segment = []
        # For the dash //

        for row in range(board.num_to_connect -1, board.height):
            for col in range(board.width - 3):

                flag = True
                sub_row = 0
                sub_col = 0
                for i in range(board.num_to_connect):

                    if board.get_cell_value(row + sub_row, col + sub_col) != self.id:
                        flag = False
                        break
                    sub_row -= 1
                    sub_col += 1


                sub_row = 0
                sub_col = 0
                if flag == True:
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

                    if board.get_cell_value(row + sub, col + sub) != self.id:
                        flag = False
                        break
                    sub += 1

                sub = 0
                if flag == True:
                    dia_segment = Segment()
                    for i in range(board.num_to_connect):
                        dia_segment.add_pos([row + sub, col + sub])
                        sub += 1
                    all_dia_correct_segment.append(dia_segment)

        return all_dia_correct_segment


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
