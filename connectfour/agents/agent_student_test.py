from connectfour.agents.agent_student import StudentAgent
from connectfour.board import Board
import numpy as np

agent_student = StudentAgent("Sample Name")
agent_student.id = 1

simple_board = Board()

for j in range(1):
    for i in range(2):
        simple_board = simple_board.next_state(agent_student.id, i)
for j in range(1):
    for i in range(2):
        simple_board = simple_board.next_state(2, i)

print(np.matrix(simple_board.board))

print(agent_student.evaluateBoardState(simple_board))



#At standard Connect Four board, there are 69 win segments at board, which is 24 horizontal
#segment (H), 21 vertical segments (V) and 24 diagonal segments (D). Each segment consists of four
