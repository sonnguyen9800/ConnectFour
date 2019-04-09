# RMIT AI - Connect4

![screenshot](https://github.com/StevenKorevaar/ai1901-connectfour/blob/master/img/game_example-small.gif)

## About The Game

Connect 4 is a two-player game in which the players take turns dropping colored discs from the top into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the next available space within the column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own discs.


## Setup

### Prerequisites

The code was written in **Python 3.6**. 

In order to display the game's GUI, we used [Tkinter](https://docs.python.org/3/library/tkinter.html) module, which is the standard Python interface to the Tk GUI toolkit. 
You most probably don't need to download Tkinter, since it is an integral part of all Python distributions. In any case, you can find more details about Tkinter installation [here](http://ftp.ntua.gr/mirror/python/topics/tkinter/download.html).

### Installation

1. Project dependencies are managed by [`pipenv`](https://github.com/pypa/pipenv). So make sure it `pipenv` is already installed in your system (e.g., `pip install pipenv -user`)
     * Check [Pipenv: A Guide to the New Python Packaging Tool
](https://realpython.com/pipenv-guide)
2. Do `pipenv install --skip-lock --dev` to install everything. (currently `--skip-lock` is used because Pipenv is failing to handle `black`)
2. Ensure Tkinter has correctly installed (follow instructions in link in 'Prerequisites' section)

### Testing

Run `pipenv run python -m pytest tests/` (You can omit `pipenv run` if you're in a `pipenv shell`)

### Linting and Code Formatting

This project uses [`black`](https://github.com/ambv/black) to keep code neat and standardised. It should already have been installed during project installation (see [Installation](#installation) section).

Run `black` with: `pipenv run black connectfour tests` (You can omit `pipenv run` if you're in a `pipenv shell`)



## Game Basics - Configuration, CLI, GUI

### Run

1. `git clone https://github.com/stevenkorevaar/ai1901-connectfour.git`
2. `cd rmit-connectfour`
3. `pipenv install` (this will install all dependencies needed) 
4. `pipenv shell` (activate the virtual environment for the project/directory)
    * To deactivate/exit from the environment just type `exit` or `Control-D`.
4. `python -m connectfour.game` (default configuration will be run; both players are human players)


### Player Agent Types

Currently this game allows only for the specification of particular player types for each player. This is done with the `--player-one XXX` and `--player-two YYY` options. 

Player agents are located in `connectfour/agents` and are subclasses of agent class `Agent`.


The currently available player types are:

* `HumanPlayer` - Player is controlled by user via GUI **[DEFAULT OPTION]**
* `RandomAgent` - Player is controlled by computer and just chooses random valid columns to place token
* `MonteCarloAgent` - Player is controlled by computer and uses Monte Carlo Tree Search to find a good move
* `StudentAgent` - Template player to complete by students. Currently, is a  `RandomAgent`


As an example to have a `RandomAgent` play against yourself, we can run:

`python -m connectfour.game --player-one RandomAgent --player-two HumanPlayer`

This next one may be useful for you to run games in quick succession to see how your agent performs against the random agent.

`python -m connectfour.game --player-one RandomAgent --player-two StudentAgent --no-graphics --fast --auto-close`


### Options

Run the program with option `-h` to get the options available:

```
[ssardina@Thinkpad-X1 pconnect4-base.git]$ python -m connectfour.game  -h
usage: game.py [-h] [--player-one PLAYER_ONE] [--player-two PLAYER_TWO]
               [--board-height [4-100]] [--board-width [4-100]] [--fast]
               [--no-graphics] [--auto-close]

Set up the game.

optional arguments:
  -h, --help            show this help message and exit
  --player-one PLAYER_ONE
                        Set the agent for player one of the game
  --player-two PLAYER_TWO
                        Set the agent for player two of the game
  --board-height [4-100]
                        Set the number of rows in the board
  --board-width [4-100]
                        Set the number of columns in the board
  --fast                disables the delay between computer moves, making the
                        game much faster.
  --no-graphics         No graphics display for Connect4 game.
  --auto-close          Shutdown the program after then game ends in a win or
                        draw.
```


### Post-game Console Output

In order to facilitate running auto-grader scripts against this program, it will output JSON formatted game result data on game exit. It's structure is as follows:

```
{
  "end_state": "win" | "draw",
  "winner_id": 1 | 2 | null,
  "num_moves": INT
}
```


## Credit, Acknowledgements & Background

This project began as a fork of [Alfo5123/Connect4](https://github.com/Alfo5123/Connect4) as part of work done for RMIT University course support for the [*COSC1125/COSC1127 Artificial Intelligence*](http://www1.rmit.edu.au/courses/004123) subject.  

The code was refactored and functionality was extended by [Jonathon Belotti](https://github.com/thundergolfer) under the guidance of A/Prof. Sebastian Sardina in charge of the RMIT AI course. The improvements & functionalities added are:

* Migration to latest Python 3.6.
* Skeleton code available (for students to elaborate).
* Headless execution (i.e., no GUI).
* Fast execution (i.e., no delays).
* Change of board size.
* Dump of game statistics into a JSON file.


The code was refactored and functionality was extended by [Steven Korevaar](https://github.com/StevenKorevaar) under the guidance of A/Prof. Xiaodong Li in charge of the RMIT AI course. The improvements & functionalities added are:

* Dynamic loading of agents to allow for automated testing 
* Tracking and outputing moves made throughout a game
* Added standard minimax agent (without evaluation function for students to start with)
* Fixed board.next_state(), winner(), and terminal() functions

