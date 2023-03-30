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


def piece_translator(piece):
    """ Function takes in a code for a piece and returns the corresponding character, as described above. 
    If the input is not -2, -1, 0, 1, 2, raises a TypeError or ValueError as needed. 
    """
    if type(piece) is not int:
        raise TypeError('Expects piece input as an integer')
    match piece:
        case -2:
            return 'X'
        case -1:
            return 'x'
        case 0:
            return ' '
        case 1:
            return 'o'
        case 2:
            return 'O'
        case other:
            raise ValueError('Valid piece inputs are -2, -1, 0, 1, 2')


def visualize_board(board):
    """ Function takes in a board state encoded as described above (a length 32 list with -2, -1, 0, 1, 2 as entries)
    and returns a string visualizing it as a checkers board.
    If the list encoding the board is not valid, raises TypeError or ValueError as needed. 
    """

    # Checks for valid board encoding
    if type(board) is not list:
        raise TypeError('Expects board input as a list of length 32')
    elif len(board) != 32:
        raise TypeError('Expects board input as a list of length 32')
    else:
        for piece in board:
            if piece not in (-2, -1, 0, 1, 2):
                raise ValueError('Valid entries in board input are -2, -1, 0, 1, 2')
    
    # Constructs board string
    board_string = ''
    for row in range(8):
        for column in range(4):
            if row % 2 == 0:
                board_string += '| |' + piece_translator(board[row * 4 + column])
            else:
                board_string += '|' + piece_translator(board[row * 4 + column]) + '| '
        if row != 7:
            board_string += '|\n'
        else:
            board_string += '|'
    return board_string


def target_position(position, move_direction):
    """ This method takes in an integer 0 - 31 move_position and an integer 0 - 3 move_direction.
    The move_direction corresponds to the following directions, when the board is illustrated as shown above:
    0 - northeast
    1 - northwest
    2 - southwest
    3 - southeast.
    This method returns the index for the square corresponding to this move (not considering jumps) if it exists,
    or returns -1 if the square does not exist (i.e. would not be on the board). If either input is invalid, 
    raises TypeError or ValueError as needed.
    """

    # check for invalid inputs
    if type(position) is not int:
        raise TypeError('Expects position input as an integer')
    elif type(move_direction) is not int:
        raise TypeError('Expects move_direction input as an integer')
    elif position not in range(32):
        raise ValueError('Valid position inputs are integers 0 to 31')
    elif move_direction not in range(4):
        raise ValueError('Valid move_direction inputs are 0, 1, 2, 3')

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


class Gamestate():
    """ The Gamestate class represents the board and some information needed to accurately and completely represent a state of the game.
    The attributes are:
        - board: a list with 32 integers representing the position of the pieces as described above
        - turn: an integer that takes on values 1 and -1; 1 indicates team 1 while -1 indicates team 2
        - continuation: multiple jumps are handled as multiple turns in which the turn does not move to the next team. However, 
          if there are multiple pieces that can jump, if one piece previously made a jump, it must continue its multiple jump. Thus,
          we need an indication of which piece must move next. This property is an integer 0 - 31 indicating the index
          of the piece that must continue jumping, while -1 indicates that there is no such piece.    
    """

    def __init__(self):
        self._board = [ 1,  1,  1,  1,
                        1,  1,  1,  1,
                        1,  1,  1,  1,
                        0,  0,  0,  0,
                        0,  0,  0,  0,
                       -1, -1, -1, -1,
                       -1, -1, -1, -1,
                       -1, -1, -1, -1]  # Starting board
        self._turn = 1                  # Team 1 goes first
        self._continuation = -1

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, new_board):
        """ This method sets the board to the given new_board, after first checking that the new_board is a list of 32
            elements consisting of (-2, -1, 0, 1, 2). It also checks that no team 2 man is at the top of the board 
            and no team 1 man is at the bottom of the board (should be a king). If the new board is not valid, it
            raise the appropriate error.
        """

        if type(new_board) is not list:
            raise TypeError('Expected new_board input as a list of length 32')
        elif len(new_board) != 32:
            raise TypeError('Expected new_board input as a list of length 32')
        else:
            for position in range(32):
                if new_board[position] not in (-2, -1, 0, 1, 2):
                    raise ValueError('Valid pieces are -2, -1, 0, 1, 2')
            for end_position in range(4):
                if new_board[end_position] == -1 or new_board[31 - end_position] == 1:
                    raise ValueError('Pieces that are not kings cannot be in their end row')
        self._board = new_board

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, new_turn):
        if type(new_turn) is not int:
            raise TypeError('Expected new_turn input as an integer')
        elif new_turn not in (-1, 1):
            raise ValueError('Valid new_turn inputs are -1 and 1')
        self._turn = new_turn

    @property
    def continuation(self):
        return self._continuation
    
    @continuation.setter
    def continuation(self, new_continuation):
        if type(new_continuation) is not int:
            raise TypeError('Expected new_continuation input as an integer')
        elif new_continuation not in range(-1, 32):
            raise ValueError('Valid new_continuation inputs are integers -1 to 31')
        self._continuation = new_continuation
    
    def piece_can_jump(self, position, move_direction):
        """ This method returns True if there is a piece in the given position that can jump in the given direction
        and False otherwise. The essential conditions to be checked is that the position to be jumped over and the 
        position to be jumped to must both be valid positions, there must be a piece of the opposing team to be 
        jumped over and a free space to land on.
        """

        # check for invalid inputs
        if type(position) is not int:
            raise TypeError('Expects position input as an integer')
        elif type(move_direction) is not int:
            raise TypeError('Expects move_direction input as an integer')
        elif position not in range(32):
            raise ValueError('Valid position inputs are integers 0 to 31')
        elif move_direction not in range(4):
            raise ValueError('Valid move_direction inputs are 0, 1, 2, 3')

        # Calculate the positions in each direction; jump has one step in the direction, while target has two.
        # If either is an invalid square, return False
        jump = target_position(position, move_direction)
        if jump == -1:
            return False
        else:
            target = target_position(jump, move_direction)
            if target == -1:
                return False

        if self.board[position] == 1:
            # Team 1 man can jump southwest or southeast
            if move_direction in (2, 3):
                if self.board[jump] in (-1, -2) and self.board[target] == 0:
                    return True
            return False
        elif self.board[position] == 2:
            # Team 1 king can jump any direction
            for move_direction in (0, 1, 2, 3):
                if self.board[jump] in (-1, -2) and self.board[target] == 0:
                    return True
            return False
        elif self.board[position] == -1:
            # Team 2 man can jump northwest or northeast
            for move_direction in (0, 1):
                if self.board[jump] in (1, 2) and self.board[target] == 0:
                    return True
            return False
        elif self.board[position] == -2:
            # Team 2 king can jump any direction
            for move_direction in (0, 1, 2, 3):
                if self.board[jump] in (1, 2) and self.board[target] == 0:
                    return True
            return False
        else:
            return False
    
    def is_valid(self, position, move_direction):
        """ This method takes in an integer 0 - 31 position and an integer 0 - 3 move_direction.
        The move_direction corresponds to the following directions, when the board is illustrated as shown above:
        0 - northeast
        1 - northwest
        2 - southwest
        3 - southeast.
        Depending on if the move is valid for this particular gamestate, the method returns true or false.
        """

        # check for invalid inputs
        if type(position) is not int:
            raise TypeError('Expects position input as an integer')
        elif type(move_direction) is not int:
            raise TypeError('Expects move_direction input as an integer')
        elif position not in range(32):
            raise ValueError('Valid position inputs are integers 0 to 31')
        elif move_direction not in range(4):
            raise ValueError('Valid move_direction inputs are 0, 1, 2, 3')

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

    def get_valid_moves(self):
        """ This method assesses the gamestate and returns a list of all valid moves. Individual moves are themselves a list,
        with the first entry the position (integer 0 - 31) and the second entry the direction (integer 0 - 3).
        If there are no valid moves, the method returns an empty list.
        """     

        valid_move_list = []

        # Iterate through all possible moves
        for position in range(32):
            for move_direction in range(4):
                if self.is_valid(position, move_direction):
                    valid_move_list.append([position, move_direction])

        return valid_move_list
        
        
class CheckersMatch():
    """ The CheckersMatch object represents a single match of checkers. It notes the current state of the game as a Gamestate object, and has 
    methods to update it as moves are fed in. It also tracks turns and moves for the purpose of determining if the game is 
    won, lost, or drawn.

    The moves lists are encoded as a nested list, so that the length of the move lists correspond to the turn count. The format is:
    [position 1, move_direction 1, position 2, move_direction 2, position 3, move_direction 3, ...]
    where moves 2, 3, etc. are a series of jumps in the same turn, should they exist.
    """

    def __init__(self):
        self._current_gamestate = Gamestate()
        self._team_1_moves = []
        self._team_2_moves = []
        self._turns_since_capture = 0 

    @property
    def current_gamestate(self):
        return self._current_gamestate
    
    @current_gamestate.setter
    def current_gamestate(self, new_gamestate):
        if type(new_gamestate) is not Gamestate:
            raise TypeError('Expected new_gamestate input as a Gamestate object')
        self._current_gamestate = new_gamestate
    
    @property
    def team_1_moves(self):
        return self._team_1_moves
    
    @team_1_moves.setter
    def team_1_moves(self, new_moves):
        """ This method checks that the given new_moves input is of the encoding outlined in the docstring of the 
        CheckersMatch class.
        """

        if type(new_moves) is not list:
            raise TypeError('Expected new_moves input as a list')
        for move in new_moves:
            if type(move) is not list:
                raise TypeError('Expected new_moves input as a nested list')
            if len(move) % 2 != 0 or len(move) == 0:
                raise TypeError('Individual moves should have even length and be nonempty')
            for i in range(len(move)):
                if i % 2 == 0 and move[i] not in range(32):
                    raise ValueError("Even entries are integers in range 0 to 31")
                elif i % 2 == 1 and move[i] not in range(4):
                    raise ValueError("Odd entries are integers in range 0 to 3")
        self._team_1_moves = new_moves

    @property
    def team_2_moves(self):
        return self._team_2_moves
    
    @team_2_moves.setter
    def team_2_moves(self, new_moves):
        """ This method checks that the given new_moves input is of the encoding outlined in the docstring of the 
        CheckersMatch class.
        """

        if type(new_moves) is not list:
            raise TypeError('Expected new_moves input as a list')
        for move in new_moves:
            if type(move) is not list:
                raise TypeError('Expected new_moves input as a nested list')
            if len(move) % 2 != 0 or len(move) == 0:
                raise TypeError('Individual moves should have even length and be nonempty')
            for i in range(len(move)):
                if i % 2 == 0 and move[i] not in range(32):
                    raise ValueError("Even entries are integers in range 0 to 31")
                elif i % 2 == 1 and move[i] not in range(4):
                    raise ValueError("Odd entries are integers in range 0 to 3")
        self._team_2_moves = new_moves

    @property
    def turns_since_capture(self):
        return self._turns_since_capture
    
    @turns_since_capture.setter
    def turns_since_capture(self, new_count):
        if type(new_count) is not int:
            raise TypeError('Expected new_count input as an integer')
        self._turns_since_capture = new_count
    
    def get_turn_count(self, team):
        """Returns the number of turns taken by the designated team, as the length of the respective moves list
        if the input is not 1 or -1, raises the appropriate error.
        """

        if type(team) is not int:
            raise TypeError('Expected team input as an integer')

        if team == 1:
            return len(self._team_1_moves)
        elif team == -1:
            return len(self._team_2_moves)
        else:
            raise ValueError('Valid team inputs are 1 and -1')
    
    def update_gamestate(self, position, move_direction):
        """ This method takes in an integer position in 0 - 31 corresponding to a square on the board and an integer move_direction 
        corresponding to the following directions:
        0 - northeast
        1 - northwest
        2 - southwest
        3 - southeast.
        The method uses the Gamestate object to check that the move is valid. If it is, it updates the board. If the turn changes (i.e.
        there is not another jump to be made) then it updates the turn. If there is another jump to be made, it updates the continuation.
        This method then updates team_1_moves and team_2_moves. Finally, it returns the following codes
        based on the outcome of this action:
        0 - invalid move
        1 - valid move, board updated, turn passes to next team
        2 - valid move, board updated, turn does not pass (continuation)
        If there is no capture, the turns_since_capture property is increased by 1. If there is a capture, it is set to 0.
        """

        # Check if move is valid
        try:
            if not self.current_gamestate.is_valid(position, move_direction):
                return 0
        except (TypeError, ValueError):
            return 0
        
        # Update turn lists. If there is continuation, we add onto the move instead of creating a new one
        if self.current_gamestate.continuation == -1:
            if self.current_gamestate.turn == 1:
                self.team_1_moves.append([position, move_direction])
            else:
                self.team_2_moves.append([position, move_direction])
        else:
            if self.current_gamestate._turn == 1:
                self.team_1_moves[-1].append(position)
                self.team_1_moves[-1].append(move_direction)
            else:
                self.team_2_moves[-1].append(position)
                self.team_2_moves[-1].append(move_direction)

        # Check if update is a jump or not
        if not self.current_gamestate.piece_can_jump(position, move_direction):
            # Piece cannot jump - a simple move
            target = target_position(position, move_direction)
            if self.current_gamestate.board[position] == self.current_gamestate.turn and (target // 4) == (0, 7):
                # Piece becomes king
                self.current_gamestate.board[target] = self.current_gamestate.board[position] * 2
            else:
                # Piece does not become king
                self.current_gamestate.board[target] = self.current_gamestate.board[position]
            self.current_gamestate.board[position] = 0
            # Update turn
            self.current_gamestate.turn *= -1
            self.turns_since_capture += 1
            return 1
        else:
            # Piece can jump
            jump = target_position(position, move_direction)
            target = target_position(jump, move_direction)
            # Remove jumped piece
            self.current_gamestate._board[jump] = 0
            if self.current_gamestate.board[position] == self.current_gamestate.turn and (target // 4) in (0, 7):
                # Piece becomes king - note turn always then passes
                self.current_gamestate.board[target] = self.current_gamestate.board[position] * 2
                self.current_gamestate.board[position] = 0
                self.current_gamestate.continuation = -1
                self.current_gamestate.turn *= -1
                self.turns_since_capture = 0
                return 1
            else:
                # Piece does not become king
                self.current_gamestate.board[target] = self.current_gamestate.board[position]
                self.current_gamestate.board[position] = 0
                # Check if the piece can continue jumping (continuation)
                piece = self.current_gamestate.board[target]
                direction_list = []
                for i in range(4):
                    direction_list.append(self.current_gamestate.piece_can_jump(target, i))
                if (piece == 1 and (direction_list[2] or direction_list[3])) or (piece == -1 and (direction_list[0] or direction_list[1]))\
                or (piece in (-2, 2) and (direction_list[0] or direction_list[1] or direction_list[2] or direction_list[3])):
                    # Piece can continue to jump
                    self.current_gamestate.continuation = target
                    return 2
                else:
                    # Piece cannot continue to jump
                    self.current_gamestate.continuation = -1
                    self.current_gamestate.turn *= -1
                    self.turns_since_capture = 0
                    return 1
        
    def is_game_over(self):
        """ This method checks the current_gamestate Gamestate object and associated properties in the CheckersMatch object to determine
        if the game has been won, lost, or drawn. The conditions for winning are either taking all of the opponents pieces or putting
        the opponent in a position where they cannot move. The conditions for a draw are 40 moves without a capture.
        Based on the results, this method returns the following encodings:
        -1 - Team 2 wins
        0 - Draw
        1 - Team 1 wins
        2 - Neither team wins, game continues.
        Note that this method is run directly following the update_gamestate method.
        """

        # Check to see if current player has no valid moves.
        if len(self._current_gamestate.get_valid_moves()) == 0:
            return -1 * self.current_gamestate.turn
        
        # If the current player has legal moves, the only way the game has ended is a draw.
        if self.turns_since_capture >= 80:
            # 40 "full" turns since the last capture
            return 0
        
        # Current plays has valid moves and the game has not drawn. Thus the game continues.
        return 2
        

            
            


