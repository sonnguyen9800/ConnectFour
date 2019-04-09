import argparse
from pydoc import locate

from connectfour.ui import start_game
from connectfour.board import Board
from connectfour.agents.computer_player import MonteCarloAgent, RandomAgent
from connectfour.agents.agent_student import StudentAgent
from connectfour.agents.agent import HumanPlayer
#from connectfour.agents.agent_hard import HardAgent


MAX_GAME_WIDTH = MAX_GAME_HEIGHT = 100
MIN_GAME_WIDTH = MIN_GAME_HEIGHT = 4

PLAYER_TYPE_MAP = {
    'HumanPlayer': HumanPlayer,
    'RandomAgent': RandomAgent,
    'MonteCarloAgent': MonteCarloAgent,
    'StudentAgent' : StudentAgent,
    #'HardAgent' : HardAgent,
}


class Game:
    """
    Manages the players of the Game
    """

    PLAYER_ONE_ID = 1
    PLAYER_TWO_ID = 2

    def __init__(
        self,
        player_one,
        player_two,
        board_height,
        board_width,
        fast_play=False,
        auto_close=False
    ):
        self.player_one = player_one
        self.player_two = player_two
        self.current_player = self.player_one
        self.player_one.id = self.PLAYER_ONE_ID
        self.player_two.id = self.PLAYER_TWO_ID
        self.board = Board(height=board_height, width=board_width)
        self.fast_play = fast_play
        self.exit_on_game_end = auto_close
        self.metrics = {
            'num_moves': 0,
            'all_moves': []
        }

    def change_turn(self):
        if self.current_player == self.player_one:
            self.current_player = self.player_two
        else:
            self.current_player = self.player_one
        self.metrics['num_moves'] += 1

    def reset(self):
        self.board = Board(height=self.board.height, width=self.board.width)
        self.current_player = self.player_one


def validate_args(args):
    p1 = 0
    p2 = 0

    print("player one = ", args.player_one)

    if args.player_one not in PLAYER_TYPE_MAP:
        #print("here")
        #print('connectfour.agents.'+args.player_one+'.'+args.player_one)
        #playerTest = my_import('connectfour.agents.'+args.player_one+'.'+args.player_one)
         
        p1 = locate('connectfour.agents.'+args.player_one)

        #RuntimeError("'{}' is not a valid player type".format(args.player_one))

    if args.player_two not in PLAYER_TYPE_MAP:
        p2 = locate('connectfour.agents.'+args.player_two)
        #raise RuntimeError("'{}' is not a valid player type".format(args.player_two))

    if (
        args.no_graphics and
        (args.player_one == 'HumanPlayer' or args.player_two == 'HumanPlayer')
    ):
        raise RuntimeError("Cannot have human player when running with no graphics")
    
    return p1, p2

def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def main():
    parser = argparse.ArgumentParser(description="Set up the game.")
    parser.add_argument(
        "--player-one",
        dest="player_one",
        action="store",
        default="HumanPlayer",
        help="Set the agent for player one of the game",
    )
    parser.add_argument(
        "--player-two",
        dest="player_two",
        action="store",
        default="HumanPlayer",
        help="Set the agent for player two of the game",
    )
    parser.add_argument(
        "--board-height",
        dest="board_height",
        action="store",
        default=None,
        type=int,
        choices=range(MIN_GAME_HEIGHT, MAX_GAME_HEIGHT),
        metavar="[{}-{}]".format(MIN_GAME_HEIGHT, MAX_GAME_HEIGHT),
        help="Set the number of rows in the board",
    )
    parser.add_argument(
        "--board-width",
        dest="board_width",
        action="store",
        default=None,
        type=int,
        choices=range(MIN_GAME_WIDTH, MAX_GAME_WIDTH),
        metavar="[{}-{}]".format(MIN_GAME_WIDTH, MAX_GAME_WIDTH),
        help="Set the number of columns in the board",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="disables the delay between computer moves, making the game much faster.",
    )
    parser.add_argument(
        "--no-graphics",
        action='store_true',
        help='No graphics display for Connect4 game.'
    )
    parser.add_argument(
        "--auto-close",
        action='store_true',
        help='Shutdown the program after then game ends in a win or draw.'
    )
    #print("Before parse args")
    args = parser.parse_args()
    #print("Before val args")
    p1, p2 = validate_args(args)

    if(p1 != 0):
        player_one = p1
    else:
        player_one = PLAYER_TYPE_MAP[args.player_one]("Player 1")

    if(p2 != 0):
        player_two = p2
    else:
        player_two = PLAYER_TYPE_MAP[args.player_two]("Player 2")

    g = Game(
        player_one,
        player_two,
        args.board_height,
        args.board_width,
        args.fast,
        args.auto_close
    )
    start_game(g, graphics=(not args.no_graphics))


if __name__ == "__main__":
    main()
