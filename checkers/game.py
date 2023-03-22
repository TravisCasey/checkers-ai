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


class gamestate():
    def __init__(self):
        self.board = [ 1,  1,  1,  1,
                       1,  1,  1,  1,
                       1,  1,  1,  1,
                       0,  0,  0,  0,
                       0,  0,  0,  0,
                      -1, -1, -1, -1,
                      -1, -1, -1, -1,
                      -1, -1, -1, -1,]  # Starting board
        self.turn = 1                   # Team 1 goes first

    def get_board(self):
        return self.board
    
    def get_turn(self):
        return self.turn
    
    def viz_board(self):
        # This method returns the current board state as a text string that looks like
        # a checkers board.
        
        board_string = ""

        for row in range(8):
            for column in range(4):
                if row % 2 == 0:
                    board_string += "| |"
    


# Test Code

game = gamestate()
print(game.get_board())
print(game.get_turn())