"""Handles backend logic of playing a match of checkers.

Facilitates a match of checkers when passed moves. This includes
checking if a move is valid, and if so, updating the gamestate to the
next. Upon conclusion of an individual game, then handles passing to the
next game.

Classes:
    Gamestate: Stores current state of a game of checkers.
    CheckersMatch: Runs a match (multiple games) of checkers.

Functions:
    target_pos: Returns index of the target of the given move, if it is
        on the map.
"""

# TODO: Add piece_count method that returns the number of each piece as
# a tuple.


def target_pos(move):
    """Returns target square index of the given move.
     
    Args:
        move: A tuple of length two where the first entry is an integer
            in 0 - 31 representing the position of the piece to be moved
            and the second is an integer in 0 - 3 representing the
            direction of the move.
    
    Returns:
        The index of the square on the board that the move ends on, if
        it exists. Else, it returns None.
    
    Raises:
        TypeError, ValueError: If move argument is not as described
            above.
    """

    if type(move) is not tuple:
        raise TypeError('Expects move input as a tuple.')
    elif len(move) != 2:
        raise ValueError('Expects move input to have length two.')
    pos, dir = move
    if type(pos) is not int:
        raise TypeError('Expects pos input as an integer.')
    elif type(dir) is not int:
        raise TypeError('Expects dir input as an integer.')
    elif pos not in range(32):
        raise ValueError('Valid pos inputs are integers 0 to 31.')
    elif dir not in range(4):
        raise ValueError('Valid dir inputs are 0, 1, 2, 3.')

    row = pos // 4
    column = pos % 4

    # Return formulae vary by row and column. Note if the move does not
    # fulfill either criteria, then it would move off board and so
    # returns None.
    if (row % 2 == 0
            and not (row == 0 and (dir in (0, 1)))
            and not (column == 3 and (dir in (0, 3)))):
        match dir:
            case 0:
                return 4*(row-1) + column + 1
            case 1:
                return 4*(row-1) + column
            case 2:
                return 4*(row+1) + column
            case 3:
                return 4*(row+1) + column + 1
    elif (row % 2 == 1
            and not (row == 7 and (dir in (2, 3)))
            and not (column == 0 and (dir in (1, 2)))):
        match dir:
            case 0:
                return 4*(row-1) + column
            case 1:
                return 4*(row-1) + column - 1
            case 2:
                return 4*(row+1) + column - 1
            case 3:
                return 4*(row+1) + column


class Gamestate():
    """Represents the current state of a game of checkers. 
    
    Contains the board and some attributes needed to accurately and
    completely represent a current state of the game of checkers.

    Attributes:
    board: A list of 32 integers representing the positions of the
        pieces.
    turn: An integer representing the current turn; 1 indicates team 1
        while -1 indicates team 2.
    cont: An integer 0 - 31 indicating the index of the piece that must
        continue jumping, while None indicates that there is continuation.
    ply_count: The number of half-turns taken (individual moves).
    plys_since_capture: The number of half-turns since the last capture
        to implement the 40 turn draw rule.
    prev_move: A tuple containing the last full move taken (i.e. tuple
        can have length longer than two for multiple jumps).
    move_mem: A tuple storing previous moves in a multiple jump to
        record full move in prev_move.
    invalid_flag: A boolean that is True if the last attempted move was
        invalid.
    """

    # Some dictionaries used in the class methods.
    piece_dirs = {
        1: (2, 3),
        2: (0, 1, 2, 3),
        -1: (0, 1),
        -2: (0, 1, 2, 3),
        0: ()
    }
    team_pieces = {
        1: (1, 2),
        -1: (-1, -2)
    }
    opp_pieces = {
        1: (-1, -2),
        2: (-1, -2),
        -1: (1, 2),
        -2: (1, 2)
    }
    piece_reps = {
        1: 'o',
        2: 'O',
        -1: 'x',
        -2: 'X',
        0: ' '
    }

    def __init__(self):
        """Initializes the beginning of a checkers game."""
        self.board = [1,  1,  1,  1,
                      1,  1,  1,  1,
                      1,  1,  1,  1,
                      0,  0,  0,  0,
                      0,  0,  0,  0,
                      -1, -1, -1, -1,
                      -1, -1, -1, -1,
                      -1, -1, -1, -1]
        self.turn = 1
        self.cont = None
        self.ply_count = 0
        self.plys_since_capture = 0
        self.prev_move = None
        self.move_mem = ()
        self.invalid_flag = False

    @property
    def turn_count(self):
        return self.ply_count // 2

    def viz_board(self):
        """Visualizes the board.
        
        Returns:
            A string displaying the current board and whose turn it is.
            If a multiple jump needs to be made, instead tells to jump
            again and displays the position of the piece that must jump.
        """

        board_str = ''
        for row in range(8):
            for column in range(4):
                if row % 2 == 0:
                    board_str += '| |'
                    board_str += self.piece_reps[self.board[4*row + column]]
                else:
                    board_str += '|'
                    board_str += self.piece_reps[self.board[4*row + column]]
                    board_str += '| '
            board_str += '|\n'

        if self.cont is not None:
            board_str += 'Jump again! ({})'.format(self.cont)
        elif self.turn == 1:
            board_str += 'Team 1 turn.'
        else:
            board_str += 'Team 2 turn.'
        return board_str

    def is_jump(self, move):
        """Tests if a given move is a jump.

        Args:
            move: A tuple representing a single move. The first entry is
            a position and the second a direction.
         
        Returns:
            True if there is a piece in the position entry of the move
            that can jump in the direction entry of the move. Else,
            returns False.
        """

        pos, dir =  move
        # Index jump has one step in the given direction, while target
        # has two. If either is an invalid square, return False
        jump = target_pos(move)
        if jump is None:
            return False
        else:
            target = target_pos((jump, dir))
            if target is None:
                return False

        piece = self.board[pos]
        if (dir in self.piece_dirs[piece]
                and self.board[jump] in self.opp_pieces[piece]
                and self.board[target] == 0):
            return True
        else:
            return False

    def can_jump(self, pos):
        """Tests if there is a piece that can jump.

        Args:
            pos: An integer corresponding to a square on the board.
         
        Returns:
            True if there is a piece at the given position that can jump
            in some direction, and False otherwise.
        """

        piece = self.board[pos]
        for dir in self.piece_dirs[piece]:
            jump = target_pos((pos, dir))
            if jump is None:
                continue
            else:
                target = target_pos((jump, dir))
                if target is None:
                    continue
            if (self.board[jump] in self.opp_pieces[piece]
                    and self.board[target] == 0):
                return True
        return False

    def is_valid(self, move):
        """Tests if a given move is valid.

        Args:
            move: A tuple representing a single move. The first entry is
            a position and the second a direction.
        
        Returns:
            True if the move is valid for the current gamestate, and
            False otherwise.
        
        Raises:
            TypeError, ValueError: If move argument is not of the
            correct format.
        """

        if type(move) is not tuple:
            raise TypeError('Expects move input as a tuple.')
        elif len(move) != 2:
            raise ValueError('Expects move input to have length two.')
        pos, dir = move
        if type(pos) is not int:
            raise TypeError('Expects pos input as an integer.')
        elif type(dir) is not int:
            raise TypeError('Expects dir input as an integer.')
        elif pos not in range(32):
            raise ValueError('Valid pos inputs are integers 0 to 31.')
        elif dir not in range(4):
            raise ValueError('Valid dir inputs are 0, 1, 2, 3.')

        piece = self.board[pos]
        if piece not in self.team_pieces[self.turn]:
            return False

        if not (self.cont is None or self.cont == pos):
            return False

        # If the piece can jump and there is no continuation, the logic
        # in the is_jump module ensures that the move is valid.
        if self.is_jump(move):
            return True
        else:
            # Check if other pieces can jump
            for test_pos in range(32):
                if (self.board[test_pos] in self.team_pieces[self.turn]
                        and self.can_jump(test_pos)):
                    return False

        # There are no pieces that can jump.
        target = target_pos(move)
        if target is not None:
            if self.board[target] == 0:
                # There is a valid, empty square to move to.
                if dir in self.piece_dirs[piece]:
                    return True

        return False

    def get_valid_moves(self):
        """Returns all valid moves.
         
        Returns:
            A list of all valid moves from this gamestate. The moves are
            represented as tuples of length two.
        """
        valid_moves = []
        # Iterate through all possible moves
        for pos in range(32):
            for dir in range(4):
                if self.is_valid((pos, dir)):
                    valid_moves.append((pos, dir))
        return valid_moves

    def update(self, move):
        """Updates the gamestate with the given move.

        Note that this method assumes the move is already valid; it is
        recommended to run the is_valid method first to avoid errors.
        """
        
        pos, dir = move

        if not self.is_jump(move):
            target = target_pos(move)
            if self.board[pos] == self.turn and (target // 4) in (0, 7):
                # Piece becomes king
                self.board[target] = self.board[pos] * 2
            else:
                # Piece does not become king
                self.board[target] = self.board[pos]
            self.board[pos] = 0
            self.turn *= -1
            self.ply_count += 1
            self.plys_since_capture += 1
            self.prev_move = move

        else:
            jump = target_pos(move)
            target = target_pos((jump, dir))
            self.board[jump] = 0

            if self.board[pos] == self.turn and (target // 4) in (0, 7):
                # Piece becomes king - note turn always then passes
                self.board[target] = self.board[pos] * 2
                self.board[pos] = 0
                self.cont = None
                self.turn *= -1
                self.ply_count += 1
                self.plys_since_capture = 0
                self.prev_move = self.move_mem + move
                self.move_mem = ()

            else:
                # Piece does not become king
                self.board[target] = self.board[pos]
                self.board[pos] = 0
                # Check for continuation
                if self.can_jump(target):
                    self.cont = target
                    self.move_mem += move
                else:
                    self.cont = None
                    self.turn *= -1
                    self.ply_count += 1
                    self.plys_since_capture = 0
                    self.prev_move = self.move_mem + move
                    self.move_mem = ()

    def is_game_over(self):
        """Tests whether the game has been won by either team or drawn.

        The condition for loss is to have no valid moves. The condition
        for a draw is for 40 turns to pass without a capture.

        Returns:
            -1: Team 2 wins
            0: Draw
            1: Team 1 wins
            2: Neither team wins, game continues.
        """

        if not self.get_valid_moves():
            return -1 * self.turn

        if self.plys_since_capture >= 80:
            # 40 turns since the last capture
            return 0

        return 2

    def copy(self):
        """Returns a deep copy of the gamestate.
        
        Returns:
            A Gamestate object with identical attributes to the current
            object, though the board object is distinct.
        """

        copy_gamestate = Gamestate()
        copy_gamestate.board = self.board[:]
        copy_gamestate.turn = self.turn
        copy_gamestate.cont = self.cont
        copy_gamestate.ply_count = self.ply_count
        copy_gamestate.plys_since_capture = self.plys_since_capture
        copy_gamestate.prev_move = self.prev_move
        copy_gamestate.move_mem = self.move_mem
        return copy_gamestate

    def get_full_moves(self):
        """Returns all valid moves including multiple jumps.
        
        Returns:
            A list of all valid moves from this gamestate. The moves are
            tuples of even length, where lengths longer than two are
            multiple jumps.
        """
        full_moves = []
        valid_moves = self.get_valid_moves()
        for move in valid_moves:
            test_gamestate = self.copy()
            test_gamestate.update(move)
            if test_gamestate.cont is not None:
                for cont_move in test_gamestate.get_full_moves():
                    full_moves.append(move + cont_move)
            else:
                full_moves.append(move)

        return full_moves


class CheckersMatch():
    """A match of checkers, containing a specified amount of games.
     
    Handles both the gameplay loop over a single game and the match loop
    over (possibly) multiple games of checkers. It tracks the score of
    each player.
        
    Attributes:
    gamestate: A Gamestate object that tracks and updates the
        current state of the current checkers game.
    player_1: An instance of the Player class or subclass thereof from
        the players module. Supplies moves for team 1.
    player_2: Same as player_1, but controls team 2.
    game_count: The total number of games to be played.
    played_count: The number of games played so far.
    wins_1: The number of games in the match won by team 1.
    wins_2: The number of games in the match won by team 2.
    draws: The number of draws in the match.
    score_1: The score for team 1, where a win is 1 point and a draw is
        0.5 points.
    score_2: Same as score_1 but for team 2.
    best_of: A boolean, where True indicates the match is a "best of"
        system.
    """

    def __init__(self, player_1, player_2, game_count, best_of):
        """Initializes the checkers match.
        
        Args:
            player_1: An instance of the Player class or subclass thereof from
                the players module. Supplies moves for team 1.
            player_2: Same as player_1, but controls team 2.
            game_count: The total number of games to be played.
            best_of: A boolean, where True indicates the match is a "best of"
                system.
        
        Raises:
            TypeError: If game_count is not an integer or best_of is not
                a boolean.
            ValueError: If game_count is not at least 1.
        """

        if type(game_count) is not int:
            raise TypeError('Expected game_count input as an integer.')
        elif type(best_of) is not bool:
            raise TypeError('Expected best_of input as a boolean.')
        elif game_count < 1:
            raise ValueError('game_count should be at least 1.')
        
        self.gamestate = None
        self.player_1 = player_1
        self.player_2 = player_2
        self.game_count = game_count
        self.played_count = 0
        self.wins_1 = 0
        self.wins_2 = 0
        self.draws = 0
        self.score_1 = 0
        self.score_2 = 0
        self.best_of = best_of

    def game_loop(self):
        """The loop over moves in each individual game of checkers.

        Each iteration of the loop is a single move, which may not be a
        full ply if there is continuation.

        Returns:
        -1: Team 2 wins.
        0: Draw
        1: Team 1 wins.
        """
        while True:
            result = self.gamestate.is_game_over()
            if result != 2:
                return result

            if self.gamestate.turn == 1:
                current_player = self.player_1
            else:
                current_player = self.player_2

            next_move = current_player.get_next_turn()
            if not self.gamestate.is_valid(next_move):
                self.gamestate.invalid_flag = True
                continue
            else:
                self.gamestate.invalid_flag = False
                self.gamestate.update(next_move)

    def is_match_over(self):
        """Tests whether the match is over.

        Returns:
            True if the match is over and False otherwise.
        """
        if self.best_of:
            if max(self.score_1, self.score_2) >= self.game_count / 2:
                return True
        else:
            if self.played_count == self.game_count:
                return True
        return False

    def match_loop(self):
        """The loop over the games of checkers in the match.

        Each iteration of the loop is a single game of checkers.

        Returns:
            A tuple containing the score for team 1, the score for team
            2, team 1 wins, team 2 wins, and draws, in that order.
        """
        while not self.is_match_over():
            self.gamestate = Gamestate()
            self.player_1.gamestate = self.gamestate
            self.player_2.gamestate = self.gamestate

            game_result = self.game_loop()
            match game_result:
                case 1:
                    self.wins_1 += 1
                    self.score_1 += 1
                case -1:
                    self.wins_2 += 1
                    self.score_2 += 1
                case 0:
                    self.draws += 1
                    self.score_1 += 0.5
                    self.score_2 += 0.5
            self.played_count += 1

        return (
            self.score_1,
            self.score_2,
            self.wins_1,
            self.wins_2,
            self.draws
            )
