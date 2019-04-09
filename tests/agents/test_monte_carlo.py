from connectfour.agents.monte_carlo import Node
from connectfour.board import Board


class TestNode:
    board = Board()

    def test_add_child(self):
        node = Node(self.board)
        child_state = self.board  # TODO really should be a different board state
        move = 3

        node.add_child(child_state, move)

        assert len(node.children) is 1
        assert type(node.children[0]) is Node
        assert len(node.children_move) is 1
        assert node.children_move[0] is 3

    def test_update(self):
        node = Node(self.board)
        # initial values
        assert 0.0 == node.reward
        assert 1 == node.visits

        node.update(3.3)
        assert 3.3 == node.reward
        assert 2 == node.visits

        node.update(0.1)
        assert 3.4 == node.reward
        assert 3 == node.visits
