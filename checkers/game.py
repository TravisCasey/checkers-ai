import numpy as np

""" 
Initial checker board:

| |o| |o| |o| |o|
|o| |o| |o| |o| |
| |o| |o| |o| |o|
| | | | | | | | |
| | | | | | | | |
|x| |x| |x| |x| |
| |x| |x| |x| |x|
|x| |x| |x| |x| |

Team 1 are the o/O pieces while Team 2 are the x/X pieces

Piece Representation:

Team 1 Man  o  1
Team 1 King O  2
Team 2 Man  x  -1
Team 2 King X  -2

Blank squares are represented by 0.

As checker pieces can only move on 32 of the 64 squares, we collapse the board and use the following
indexing:

| 0| 1| 2| 3|
| 4| 5| 6| 7|
| 8| 9|10|11|
|12|13|14|15|
|16|17|18|19|
|20|21|22|23|
|24|25|26|27|
|28|29|30|31|

Team 1 turn represented by 1 while Team 2 turn represented by -1.
 """

def piece_translator(piece_number):
    # Function takes in a code for a piece and returns the corresponding character, as described above. 
    # If the number is not -2, -1, 0, 1, 2, returns error.
    match piece_number:
        case -2:
            return "X"
        case -1:
            return "x"
        case 0:
            return " "
        case 1:
            return "o"
        case 2:
            return "O"
        case other:
            return "error"


def vizualize_board(board):
    # Function takes in a board state encoded as described above (a length 32 list with -2, -1, 0, 1, 2 as entries)
    # and returns a string visualizing it as a checkers board.
    # If the list encoding the board is not valid, returns "error"
    if len(board) != 32:
        return "error"
    board_string = ""
    for row in range(8):
        for column in range(4):
            if row % 2 == 0:
                board_string += "| |" + piece_translator(board[row * 4 + column])
            else:
                board_string += "|" + piece_translator(board[row * 4 + column]) + "| "
        if row != 7:
            board_string += "|\n"
        else:
            board_string += "|"
    return board_string



class Gamestate():

    """ The Gamestate class represents the board and some information needed to accurately and completely represent a state of the game.
    The properties are:
        - board: a list with 32 integers representing the position of the pieces as described above
        - turn: an integer that takes on values 1 and -1; 1 indicates team 1 while -1 indicates team 2
        - continuation: multiple jumps are handled as multiple turns in which the turn does not move to the next team. However, 
          if there are multiple pieces that can jump, if one piece previously made a jump, it must continue its multiple jump. Thus
          we need an indication of which piece must move next. This property is a positive integer; values 0 - 31 indicate the index
          of the piece that must continue jumping, while -1 indicates there is no such piece.    
    """
    
    def __init__(self):
        self.board = [ 1,  1,  1,  1,
                       1,  1,  1,  1,
                       1,  1,  1,  1,
                       0,  0,  0,  0,
                       0,  0,  0,  0,
                      -1, -1, -1, -1,
                      -1, -1, -1, -1,
                      -1, -1, -1, -1]  # Starting board
        self.turn = 1                   # Team 1 goes first
        self.continuation = -1

    def get_board(self):
        return self.board
    
    def get_turn(self):
        return self.turn
    


