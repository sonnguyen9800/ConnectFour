from connectfour.game import Game
from connectfour.agents.computer_player import RandomAgent


class TestGame:
    player_one = RandomAgent("Player 1")
    player_two = RandomAgent("Player 2")
    height = 6
    width = 10

    def test_change_turn(self):
        game = Game(self.player_one, self.player_two, self.height, self.width)

        assert game.current_player == self.player_one
        game.change_turn()
        assert game.current_player == self.player_two
