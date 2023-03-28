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
    """ Function takes in a code for a piece and returns the corresponding character, as described above. 
    If the number is not -2, -1, 0, 1, 2, returns error. 
    """

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


def visualize_board(board):
    """ Function takes in a board state encoded as described above (a length 32 list with -2, -1, 0, 1, 2 as entries)
    and returns a string visualizing it as a checkers board.
    If the list encoding the board is not valid, returns "error" 
    """

    # Checks for valid board encoding
    if type(board) is not list:
        return "error"
    elif len(board) != 32:
        return "error"
    else:
        for position in board:
            if position not in (-2, -1, 0, 1, 2):
                return "error"
    
    # Constructs board string
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


def target_position(position, move_direction):
    """ This method takes in a positive integer move_position and an integer move_direction.
    The move_direction corresponds to the following directions, when the board is illustrated as shown above:
    0 - northeast
    1 - northwest
    2 - southwest
    3 - southeast.
    This method returns the index for the square corresponding to this move (not considering jumps) if it exists,
    or returns -1 if the square does not exist (i.e. would not be on the board). If either input is invalid, returns -1.
    """

    # check for invalid inputs
    if position not in range(32) or move_direction not in range(4):
        return -1

    row = position // 4
    column = position % 4

    if row % 2 == 0:
        if row == 0 and (move_direction == 0 or move_direction == 1):
            # off board
            return -1
        elif column == 3 and (move_direction == 0 or move_direction == 3):
            # off board
            return -1
        elif move_direction == 0:
            # Move northeast one square
            return (row - 1) * 4 + column + 1
        elif move_direction == 1:
            # Move northwest one square
            return (row - 1) * 4 + column
        elif move_direction == 2:
            # Move southwest one square
            return (row + 1) * 4 + column
        elif move_direction == 3:
            # Move southeast one square
            return (row + 1) * 4 + column + 1
    elif row % 2 == 1:
        if row == 7 and (move_direction == 2 or move_direction == 3):
            # off board
            return -1
        elif column == 0 and (move_direction == 1 or move_direction == 2):
            # off board
            return -1
        elif move_direction == 0:
            # Move northeast one square
            return (row - 1) * 4 + column
        elif move_direction == 1:
            # Move northwest one square
            return (row - 1) * 4 + column - 1
        elif move_direction == 2:
            # Move southwest one square
            return (row + 1) * 4 + column - 1
        elif move_direction == 3:
            # Move southeast one square
            return (row + 1) * 4 + column
    
    # Some other error
    return -1        


class Gamestate():
    """ The Gamestate class represents the board and some information needed to accurately and completely represent a state of the game.
    The attributes are:
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
        self.turn = 1                  # Team 1 goes first
        self.continuation = -1


    def get_board(self):
        return self.board
    

    def set_board(self, new_board):
        """ This method sets the board to the given new_board, after first checking that the new_board is a list of 32
            elements consisting of (-2, -1, 0, 1, 2). It also checks that no team 2 man is at the top of the board 
            and no team 1 man is at the bottom of the board (should be a king). 
        """

        valid_board = True
        if type(new_board) is not list:
            valid_board = False
        elif len(new_board) != 32:
            valid_board = False
        else:
            for position in range(32):
                if new_board[position] not in (-2, -1, 0, 1, 2):
                    valid_board = False
            for end_position in range(4):
                if new_board[end_position] == -1 or new_board[31 - end_position] == 1:
                    valid_board = False
        if valid_board:
            self.board = new_board
    

    def get_turn(self):
        return self.turn
    

    def set_turn(self, new_turn):
        if new_turn in (-1, 1):
            self.turn = new_turn
    

    def get_continuation(self):
        return self.continuation
    

    def set_continuation(self, new_continuation):
        if new_continuation in range(-1, 32):
            self.continuation = new_continuation
    

    def is_game_over(self): # This should be moved to the overarching game object
        # Also need to check for 40 move rule and 3 piece repetition rule. And if forced into a position with no valid moves
        """ This method checks if the current gamestate is an end position for a game, i.e., whether either team has won.
        If so, the method returns a positive integer with the following encoding:
        -2 - invalid gamestate
        0 - neither team has won
        1 - team 1 has won
        -1 - team 2 has won
        """

        """We loop through all the positions of the board. The three following booleans record if there are pieces of team 1
        present, team 2 present, or if there is an erroneous piece. 
        """

        error = False
        one_present = False
        two_present = False
        for position in self.board:
            if position == 1 or position == 2:
                one_present = True
            elif position == -1 or position == -2:
                two_present = True
            elif position != 0:
                error = True
        
        if error or not (error or one_present or two_present):
            # If there is an incorrect piece or there are no pieces at all
            return -2
        elif one_present and not two_present:
            # If there are only pieces from team 1
            return 1
        elif two_present and not one_present:
            # If there are only pieces from team 2
            return -1
        else:
            # This indicates we have a valid board yet neither team has won
            return 0
        
    
    def piece_can_jump(self, position, move_direction):
        """ This method returns True if there is a piece in the given position that can jump in the given direction
        and False otherwise. The essential conditions to be checked is that the position to be jumped over and the 
        position to be jumped to must both be valid positions, there must be a piece of the opposing team to be 
        jumped over and a free space to land on.
        """

        if position not in range(32) or move_direction not in range(4):
            return False

        # Calculate the positions in each direction; pos_1 has one step in the direction, while pos_2 has two.
        pos_1 = target_position(position, move_direction)
        if pos_1 >= 0:
            pos_2 = target_position(pos_1, move_direction)
        else:
            pos_2 = -1

        if self.board[position] == 1:
            # Team 1 man can jump southwest or southeast
            if move_direction in (2, 3):
                if pos_1 >= 0 and pos_2 >= 0 and self.board[pos_1] in (-1, -2) and self.board[pos_2] == 0:
                    return True
            return False
        elif self.board[position] == 2:
            # Team 1 king can jump any direction
            for move_direction in (0, 1, 2, 3):
                if pos_1 >= 0 and pos_2 >= 0 and self.board[pos_1] in (-1, -2) and self.board[pos_2] == 0:
                    return True
            return False
        elif self.board[position] == -1:
            # Team 2 man can jump northwest or northeast
            for move_direction in (0, 1):
                if pos_1 >= 0 and pos_2 >= 0 and self.board[pos_1] in (1, 2) and self.board[pos_2] == 0:
                    return True
            return False
        elif self.board[position] == -2:
            # Team 2 king can jump any direction
            for move_direction in (0, 1, 2, 3):
                if pos_1 >= 0 and pos_2 >= 0 and self.board[pos_1] in (1, 2) and self.board[pos_2] == 0:
                    return True
            return False
        else:
            return False
        
    
    def is_valid(self, position, move_direction):
        """ This method takes in a positive integer move_position and an integer move_direction.
        The move_direction corresponds to the following directions, when the board is illustrated as shown above:
        0 - northeast
        1 - northwest
        2 - southwest
        3 - southeast.
        Depending on if the move is valid for this particular gamestate, the method returns true or false.
        """

        if position not in range(32) or move_direction not in range(4):
            return False

        move_piece = self.board[position]

        # Check if there is a piece of the right team on the given position
        if self.turn == 1 and move_piece not in (1, 2):
            return False
        elif self.turn == -1 and move_piece not in (-1, -2):
            return False

        # Check for continuation
        if not (self.continuation == -1 or self.continuation == position):
            return False  
        
        """If the piece can jump and there is no continuation, the logic in the piece_can_jump module
        ensures that the move is valid. Else, we need to make sure that there are no other pieces that can jump;
        such a circumstance would require one of the other pieces to be moved.
        """
        if self.piece_can_jump(position, move_direction):
            return True
        else:
            for test_position in range(32):
                for test_direction in range(4):
                    if self.turn == 1 and self.board[test_position] in (1, 2) and self.piece_can_jump(test_position, test_direction):
                        return False
                    elif self.turn == -1 and self.board[test_position] in (-1, -2) and self.piece_can_jump(test_position, test_direction):
                        return False

        # There are no pieces that can jump. All that remains to check is if the piece can move normally in the given direction.
        target = target_position(position, move_direction)
        if target >= 0 and self.board[target] == 0:
            # There is a valid square to move to on the board and it is empty
            if move_piece == 1 and move_direction in (2, 3):
                # Team 1 man
                return True
            elif move_piece == -1 and move_direction in (0, 1):
                # Team 2 man
                return True
            elif move_piece in (-2, 2):
                # Team 1 or 2 King
                return True            
        else:  
            return False        
        
        
class CheckersMatch():
    """ The CheckersMatch object represents a single match of checkers. It notes the current state of the game as a Gamestate object, and has 
    methods to update it as moves are fed in. It also tracks turns and repeated moves for the purpose of determining if the game is 
    won, lost, or drawn.

    The turn_count iterates after both teams play.

    The moves lists are encoded as a nested list, so that the length of the move lists correspond to the turn_count. The format is:
    [position 1, move_direction 1, position 2, move_direction 2, position 3, move_direction 3, ...]
    where moves 2, 3, etc. are a series of jumps in the same turn, should they exist.
    """

    def __init__(self):
        current_gamestate = Gamestate()
        turn_count = 0
        team_1_moves = []
        team_2_moves = []

    
    def get_board(self);
        return self.current_gamestate.get_board()


    def get_team_1_moves(self):
        return self.team_1_moves

    
    def update_gamestate(self, position, move_direction):
        """ This method takes in an integer position in 0 - 31 corresponding to a square on the board and an integer move_direction 
        corresponding to the following directions:
        0 - northeast
        1 - northwest
        2 - southwest
        3 - southeast.
        The method uses the Gamestate object to check that the move is valid. If it is, it updates the board. If the turn changes (i.e.
        there is not another jump to be made) then it updates the turn. If there is another jump to be made, it updates the continuation.
        This method then updates the turn_count, team_1_moves, and team_2_moves, respectively. Finally, it returns the following codes
        based on the outcome of this action:
        0 - invalid move
        1 - valid move, board updated, turn passes to next team
        2 - valid move, board updated, turn does not pass (continuation)
        """

