#!/usr/bin/env python

from connectfour.agents.agent import HumanPlayer
from connectfour.util import delay_move_execution

import copy
import json
import tkinter.font
from tkinter import Frame, Canvas, Tk, Label, NSEW, Button
import time

LEFT_MOUSE_CLICK = "<Button-1>"
ROW_SPACE = int(400 / 6)
COL_SPACE = int(500 / 7)


class Info(Frame):
    """
    Message in the top of screen
    """

    def __init__(self, master=None):
        Frame.__init__(self)
        self.configure(width=500, height=100, bg="white")
        police = tkinter.font.Font(family="Arial", size=36, weight="bold")
        self.t = Label(self, text="Connect4", font=police, bg="white")
        self.t.grid(sticky=NSEW, pady=20)


class Point(object):
    """
    Each one of the circles in the board
    """

    OUTLINE_COLOR = "blue"
    RADIUS = 30

    def __init__(self, x, y, canvas, color="white"):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.turn = 1
        self.r = self.RADIUS
        self.point = self.canvas.create_oval(
            self.x + 10,
            self.y + 10,
            self.x + 61,
            self.y + 61,
            fill=color,
            outline=self.OUTLINE_COLOR,
        )

    def set_color(self, color):
        self.canvas.itemconfigure(self.point, fill=color)
        self.color = color


class Terrain(Canvas):
    """
    Board visual representation
    """

    PLAYER_ONE_TOKEN_COLOR = "yellow"
    PLAYER_TWO_TOKEN_COLOR = "red"
    EMPTY_SLOT_COLOR = "white"

    def __init__(self, game, info, master=None):
        """
        Args:
            game: An instance of `Game`, which contains player info and game state
            info: An info UI element that updates users on game state
            master: This represents the parent window. (required by Canvas superclass)
        """
        Canvas.__init__(self)

        self.p = []
        self.game = game
        self.info = info
        self.winner = False
        self.b = game.board
        self.last_bstate = self.b

        self.configure(
            width=COL_SPACE * self.b.width, height=ROW_SPACE * self.b.height, bg="blue"
        )

        for i in range(self.b.height):
            spots = []
            for j in range(self.b.width):
                spots.append(Point(j * COL_SPACE, i * ROW_SPACE, self))
            self.p.append(spots)

        self.bind(LEFT_MOUSE_CLICK, self.action)
        if not self.game.fast_play:
            self.run_computer_move = delay_move_execution(self.run_computer_move)

    def reload_board(self, i=None, j=None, val=None, bstate=None):
        """
        Reloads the board colors and content.
        Uses recursive upload for more complex cases (e.g. step back).
        [i,j,val] or [bstate] can be provided (but not simpultaneously).
        If no i, j, values or bstate are provided, it updates only colors.
        I bstate is present, updates the board values first and then colors.
        If i and j is present but no val, then updates the color of only one cell.
        If i and j and val are present, updates the matrix and the color.
        """
        if i is None:
            if bstate is not None:
                self.b = copy.deepcopy(bstate)
            for i in range(self.b.height):
                for j in range(self.b.width):
                    self.reload_board(i, j, val=None, bstate=None)
        elif val is None:
            if self.b.board[i][j] == self.game.PLAYER_ONE_ID:
                self.p[i][j].set_color(self.PLAYER_ONE_TOKEN_COLOR)
            elif self.b.board[i][j] == self.game.PLAYER_TWO_ID:
                self.p[i][j].set_color(self.PLAYER_TWO_TOKEN_COLOR)
            elif self.b.board[i][j] == 0:
                self.p[i][j].set_color(self.EMPTY_SLOT_COLOR)
        else:
            self.b.board[i][j] = val
            self.reload_board(i, j)

    def run_computer_move(self):
        row, col = self.game.current_player.get_move(self.b)
        assert self.b.valid_move(row, col)
        self.b.last_move = [row, col]
        self.game.metrics['all_moves'].append( [row, col, self.game.current_player.id] )
        self.reload_board(row, col, self.game.current_player.id)

    def action(self, event):
        self.last_bstate = copy.deepcopy(self.b)

        # Human Action
        if not self.winner:
            col = int(event.x / 71)  # TODO: magic number here
            row = self.b.try_move(col)

            if row == -1:
                return
            else:
                self.reload_board(row, col, self.game.current_player.id)

            self.b.last_move = [row, col]
            self.game.metrics['all_moves'].append( [row, col, self.game.current_player.id] )
            self.game.change_turn()
            self.set_post_move_state()
            self.update()

    def set_post_move_state(self):
        whos_turn_txt = "{}'s Turn".format(str(self.game.current_player))
        self.info.t.config(text=whos_turn_txt)

        result = self.b.winner()

        if result == self.game.PLAYER_ONE_ID:
            self.info.t.config(text="{} won!".format(self.game.player_one))
            self.winner = True
        elif result == self.game.PLAYER_TWO_ID:
            self.info.t.config(text="{} won!".format(self.game.player_two))
            self.winner = True
        elif self.b.terminal():
            self.info.t.config(text="Draw")
            self.winner = True


def game_loop(root, game, terrain):
    def inner():
        # If current player is a Human Player, we just keep waiting for a
        # UI event to trigger the move
        if type(game.current_player) is not HumanPlayer:
            terrain.run_computer_move()
            game.change_turn()
            terrain.set_post_move_state()
            terrain.reload_board()
            terrain.update()

        if not terrain.winner and not terrain.b.terminal():
            root.after(100, inner)
        elif terrain.winner and terrain.game.exit_on_game_end:
            time.sleep(1)
            run_exit(game, game.board.winner())

    return inner


def run_exit(game, result):
    output = {}
    if not result:
        output["end_state"] = "draw"
        output["winner_id"] = None
    else:
        output["end_state"] = "win"
        output["winner_id"] = result

    output["num_moves"] = game.metrics["num_moves"]
    output["all_moves"] = game.metrics["all_moves"]
    print(json.dumps(output))
    exit(0)


def run_headless_game(game):
    while True:
        row, col = game.current_player.get_move(game.board)

        game.metrics['all_moves'].append( [row, col, game.current_player.id] )

        game.board.board[row][col] = game.current_player.id
        game.change_turn()

        result = game.board.winner()
        if result or game.board.terminal():
            run_exit(game, result)


def run_graphics_game(game):
    root = Tk()
    root_height = game.board.height * ROW_SPACE
    root_width = game.board.width * COL_SPACE
    bottom_buttons_padding = 500
    root.geometry("{}x{}".format(root_width, root_height + bottom_buttons_padding))
    root.title("Connect 4 AI Bot")
    root.configure(bg="white")
    root.minsize(root_height, root_width)

    info = Info(root)
    info.grid(row=0, column=0)

    t = Terrain(game, info, root)
    t.grid(row=1, column=0)

    root.after(
        0, game_loop(root, game, t)
    )  # run game loop function as often as possible

    def close():
        root.destroy()

    Button(root, text="Exit", command=close).grid(row=4, column=0, pady=2)

    root.mainloop()


def start_game(game, graphics=True):
    if not graphics and (
        game.player_one == HumanPlayer or game.player_two == HumanPlayer
    ):
        raise RuntimeError("Cannot run without graphics if you play with a Human agent")

    if graphics:
        run_graphics_game(game)
    else:
        run_headless_game(game)
