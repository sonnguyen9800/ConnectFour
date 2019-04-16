from connectfour.agents.agent_student import StudentAgent
from connectfour.board import Board
import numpy as np

agent_student = StudentAgent("Sample Name")
agent_student.id = 1

agent_student2 = StudentAgent("Agent 2")
agent_student2.id = 2

simple_board = Board()

# for j in range(1):
#     for i in range(2):
#         simple_board = simple_board.next_state(agent_student.id, i)
# simple_board = simple_board.next_state(agent_student.id, 3)
# simple_board = simple_board.next_state(agent_student.id, 2)

#
# simple_board = simple_board.next_state(agent_student.id % 2 + 1, 3)
# simple_board = simple_board.next_state(agent_student.id % 2 + 1, 2)
# simple_board = simple_board.next_state(agent_student.id, 3)
# simple_board = simple_board.next_state(agent_student.id, 3)

simple_board.board = [
    [0,0,1,1,2,0,2],
    [0,0,2,1,2,0,1],
    [0,1,2,2,1,0,2],
    [1,2,1,1,1,0,1],
    [2,1,2,1,2,0,2],
    [2,2,2,1,2,1,1]
]

print(np.matrix(simple_board.board))
print("Player 1:")
#print(agent_student.evaluateBoardState(simple_board))
print(agent_student.evaluateBoardState(simple_board))
#print(agent_student.what_turn(simple_board))

print()
print("Player 2:")
print(agent_student2.evaluateBoardState(simple_board))
#print(agent_student2.what_turn(simple_board))


