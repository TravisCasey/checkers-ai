"""Plays matches of checkers.

Contains everything needed to play checkers. The variation is English
draughts (https://en.wikipedia.org/wiki/English_draughts).

Along with the ability to play manually, there are two other classes of
players implemented; a random player which chooses uniformly randomly
from the list of all valid moves, and a tree search player that maps
future states and chooses options leading to desirable outcomes.
Multiple difficulties are implemented in the tree search player by
specifying how many moves the player looks ahead.

Further player types may be implemented as subclasses of the provided
Player class in the players module.

A match of checkers may be played in the command line by calling the
command_line_interface function in the build module and passing a tuple
of the player classes to choose from, and passing the class of the
checkers match. The build file can be also be ran directly.

Example Usage:
    command_line_interface((players.Player,
                            players.RandomPlayer,
                            players.EasyPlayer,
                            players.MediumPlayer,
                            players.HardPlayer),
                           game.CheckersMatch)

To play a match of checkers with the backend logic but without the
command line interface, an instance of the CheckersMatch class in the
game module may be created and provided the players.

Example Usage:
    test_match = CheckersMatch(player1,
                               player2,
                               10,
                               False)
    results = test_match.match_loop()

Some implementation conventions: 

Initial checker board:

| |o| |o| |o| |o|
|o| |o| |o| |o| |
| |o| |o| |o| |o|
| | | | | | | | |
| | | | | | | | |
|x| |x| |x| |x| |
| |x| |x| |x| |x|
|x| |x| |x| |x| |

Team 1 are the o/O pieces while Team 2 are the x/X pieces.

Piece Representation:
Team 1 Man   o   1
Team 1 King  O   2
Team 2 Man   x  -1
Team 2 King  X  -2
Blank squares are represented by 0.

As checker pieces can only move on 32 of the 64 squares, we collapse the
board and use the following indexing to represent the board as a list,
with the above piece representation:

| 0| 1| 2| 3|
| 4| 5| 6| 7|
| 8| 9|10|11|
|12|13|14|15|
|16|17|18|19|
|20|21|22|23|
|24|25|26|27|
|28|29|30|31|

Team 1 turn is represented by 1 while Team 2 turn is represented by -1.
A turn refers to both teams moving, while a ply is a half-turn, i.e.,
just one team moves.

Moves are represented by tuples (pos, dir), where pos is an integer
0 - 31 that refers to the position of the piece to be moved as described
above, and dir is an integer 0 - 3 referring to directions:
0 - Northeast,
1 - Northwest,
2 - Southwest,
3 - Southeast,
when the board is oriented as above.

Singles moves with multiple jumps are called continuation. The move
input is handled as if they are multiple moves, that is, each jump in
the sequence is its own tuple. At times when the entire multi-jump move
should be represented together, these tuples are concatenated in order,
forming a tuple with even length greater than 2, alternating positions
and directions.
"""

from . import game
from . import players
