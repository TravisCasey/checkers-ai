""" This module handles most of the backend logic of playing a game of
checkers. An instance of the CheckersMatch class fetches moves from its
player attributes, which should be instances of the Player class or a
subclass thereof in the players module. It also has an associated
instance of the Gamestate object, which tracks and updates the board and
other related information.
"""
# TODO: Add piece_count method that returns the number of each piece as
# a tuple.

""" Initial checker board:

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

When a piece has jumped and can jump again, the same team is then
required to jump again (unless the original piece became a king). In
this case, the Gamestate attribute cont is set to the position
of the piece that must move again; it's default value is None when there
is no continuation. Note in this case, the turn does not pass to the
next player until the continuation is over.

The conditions for winning are forcing the opponent into a situation in
which they have no valid moves. The typical method is to simply
eliminate all the opponent's pieces, however this is not the only
possibility. A draw occurs when 40 turns have passed without a capture
(i.e. both players have moved 40 times since the last capture).
 """


def target_pos(pos, dir):
    """ This method takes in an integer 0 - 31 pos denoting the position
    of the piece to move and an integer 0 - 3 dir denoting the direction
    the piece should move. This method returns the index for the square
    corresponding to this move (not considering jumps) if it exists, or
    returns None if the square does not exist (i.e. would not be on the
    board). If either input is invalid, raises TypeError or ValueError
    as needed.
    """

    # check for invalid inputs
    if type(pos) is not int:
        raise TypeError('Expects pos input as an integer')
    elif type(dir) is not int:
        raise TypeError('Expects dir input as an integer')
    elif pos not in range(32):
        raise ValueError('Valid pos inputs are integers 0 to 31')
    elif dir not in range(4):
        raise ValueError('Valid dir inputs are 0, 1, 2, 3')

    row = pos // 4
    column = pos % 4

    # The outer conditions subdivide into even rows and columns as their
    # return formulas are different. It also checks that the pieces
    # would not move off board.
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
    """ The Gamestate class represents the board and some information
    needed to accurately and completely represent a current state of the
    game of checkers. The attributes are:
    - board: a list with 32 integers representing the position of the
      pieces as described above.
    - turn: an integer that takes on values 1 and -1; 1 indicates team 1
      while -1 indicates team 2.
    - cont: multiple jumps are handled as multiple turns in
      which the turn does not move to the next team. This property is an
      integer 0 - 31 indicating the index of the piece that must
      continue jumping, while None indicates that there is continuation.
    - ply_count: The number of half-turns taken (individual moves).
    - plys_since_capture: Tracks the number of half-turns since the last
    capture to implement the 40 turn draw rule.
    """

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

    @property
    def turn_count(self):
        return self.ply_count // 2

    def viz_board(self):
        """ This method returns a string visualizing the current
        gamestate as a checkers board.
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
            board_str += 'Jump again!'
        elif self.turn == 1:
            board_str += 'Team 1 turn.'
        else:
            board_str += 'Team 2 turn.'
        return board_str

    def is_jump(self, pos, dir):
        """ This method returns True if there is a piece in the given
        position that can jump in the given direction and False
        otherwise.
        """
        if type(pos) is not int:
            raise TypeError('Expects pos input as an integer')
        elif type(dir) is not int:
            raise TypeError('Expects dir input as an integer')
        elif pos not in range(32):
            raise ValueError('Valid pos inputs are integers 0 to 31')
        elif dir not in range(4):
            raise ValueError('Valid dir inputs are 0, 1, 2, 3')

        # Index jump has one step in the  given direction, while target
        # has two. If either is an invalid square, return False
        jump = target_pos(pos, dir)
        if jump is None:
            return False
        else:
            target = target_pos(jump, dir)
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
        """ This method takes in an integer 0 - 31 pos and tests
        if the piece in the given position can jump in any direction.
        It returns True or False based on the outcome. If there is no
        piece, returns False.
        """
        if type(pos) is not int:
            raise TypeError('Expects pos input as an integer')
        elif pos not in range(32):
            raise ValueError('Valid pos inputs are integers 0 to 31')

        piece = self.board[pos]
        for dir in self.piece_dirs[piece]:
            jump = target_pos(pos, dir)
            if jump is None:
                continue
            else:
                target = target_pos(jump, dir)
                if target is None:
                    continue
            if (self.board[jump] in self.opp_pieces[piece]
                    and self.board[target] == 0):
                return True
        return False

    def is_valid(self, pos, dir):
        """ This method takes in an integer 0 - 31 pos and an integer
        0 - 3 dir. It returns True if there is a piece of the correct
        team in the given position that can move and False otherwise.
        """
        if type(pos) is not int:
            raise TypeError('Expects pos input as an integer')
        elif type(dir) is not int:
            raise TypeError('Expects dir input as an integer')
        elif pos not in range(32):
            raise ValueError('Valid pos inputs are integers 0 to 31')
        elif dir not in range(4):
            raise ValueError('Valid dir inputs are 0, 1, 2, 3')

        piece = self.board[pos]
        if piece not in self.team_pieces[self.turn]:
            return False

        if not (self.cont is None or self.cont == pos):
            return False

        # If the piece can jump and there is no continuation, the logic
        # in the is_jump module ensures that the move is valid.
        if self.is_jump(pos, dir):
            return True
        else:
            # Check if other pieces can jump
            for test_pos in range(32):
                if (self.board[test_pos] in self.team_pieces[self.turn]
                        and self.can_jump(test_pos)):
                    return False

        # There are no pieces that can jump.
        target = target_pos(pos, dir)
        if target is not None:
            if self.board[target] == 0:
                # There is a valid, empty square to move to.
                if dir in self.piece_dirs[piece]:
                    return True

        return False

    def get_valid_moves(self):
        """ This method assesses the gamestate and returns a list of all
        valid moves. If there are no valid moves, the method returns an
        empty list.
        """
        valid_moves = []
        # Iterate through all possible moves
        for pos in range(32):
            for dir in range(4):
                if self.is_valid(pos, dir):
                    valid_moves.append((pos, dir))
        return valid_moves

    def update(self, pos, dir):
        """ This method takes in an integer 0 - 31 pos and an integer
        0 - 3 dir. The method uses the is_valid method to check that the
        move is valid. If it is, it updates the board. If the turn
        changes (i.e. no continuation) then it updates the
        ply counts. If there is another jump to be made, it updates the
        cont. Finally, it returns the following codes:
        0 - invalid move
        1 - valid move, turn passes to next team
        2 - valid move, turn does not pass (continuation)
        """
        try:
            if not self.is_valid(pos, dir):
                return 0
        except (TypeError, ValueError):
            return 0

        if not self.is_jump(pos, dir):
            target = target_pos(pos, dir)
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
            return 1
        else:
            jump = target_pos(pos, dir)
            target = target_pos(jump, dir)
            self.board[jump] = 0
            if self.board[pos] == self.turn and (target // 4) in (0, 7):
                # Piece becomes king - note turn always then passes
                self.board[target] = self.board[pos] * 2
                self.board[pos] = 0
                self.cont = None
                self.turn *= -1
                self.ply_count += 1
                self.plys_since_capture = 0
                return 1
            else:
                # Piece does not become king
                self.board[target] = self.board[pos]
                self.board[pos] = 0
                # Check for continuation
                piece = self.board[target]
                if self.can_jump(target):
                    self.cont = target
                    return 2
                else:
                    self.cont = None
                    self.turn *= -1
                    self.ply_count += 1
                    self.plys_since_capture = 0
                    return 1

    def is_game_over(self):
        """ This method checks the Gamestate object determines if the
        game has been won, lost, or drawn. Returns:
        -1 - Team 2 wins
        0 - Draw
        1 - Team 1 wins
        2 - Neither team wins, game continues.
        """
        if not self.get_valid_moves():
            return -1 * self.turn

        if self.plys_since_capture >= 80:
            # 40 "full" turns since the last capture
            return 0

        return 2

    def copy(self):
        """ This method returns a deep copy of the gamestate."""
        copy_gamestate = Gamestate()
        copy_gamestate.board = self.board[:]
        copy_gamestate.turn = self.turn
        copy_gamestate.cont = self.cont
        return copy_gamestate

    def get_full_moves(self):
        """ This method returns a list of all valid moves including
        multiple jumps which are collected in a single tuple.
        """
        full_moves = []
        valid_moves = self.get_valid_moves()
        for move in valid_moves:
            test_gamestate = self.copy()
            if test_gamestate.update(*move) == 2:
                for cont_move in test_gamestate.get_full_moves():
                    full_moves.append(move + cont_move)
            else:
                full_moves.append(move)

        return full_moves


class CheckersMatch():
    """ The CheckersMatch object represents a single match of checkers.
    It contains the current state of the game as a Gamestate object, and
    has methods to control the gameplay loop. The attributes are:
    - gamestate: A Gamestate object that tracks and updates the
    current state of the current checkers game.
    - player_1: An instance of the Player class or subclass
    thereof from the players module. Controls team 1.
    - player_2: Same as player_1, but controls team 2.
    - last_move: Holds the most recent move to be fed to the next
    player. Used for the tree search player.
    - move_memory: Used to hold the last move for the purpose of
    continuation moves, so that the entire full move can be assigned
    to last_move.
    """

    def __init__(self, player_1, player_2, game_count, best_of):
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
        self.last_move = None
        self.move_memory = ()

    def game_loop(self):
        """This method controls the game each ply. It loops until the
        game is over, then returns the result.
        """
        while True:
            result = self.gamestate.is_game_over()
            if result != 2:
                return result

            if self.gamestate.turn == 1:
                current_player = self.player_1
            else:
                current_player = self.player_2

            next_move = current_player.get_next_turn(self.last_move)
            move_result = self.gamestate.update(*next_move)

            match move_result:
                # FIXME: This module should not be printing
                case 0:
                    print('Invalid move')
                case 1:
                    self.last_move = self.move_memory + next_move
                    self.move_memory = ()
                case 2:
                    self.move_memory += next_move

    def is_match_over(self):
        """ This method checks if the match loop should terminate as
        the match is over.
        """
        if self.best_of:
            if max(self.score_1, self.score_2) >= self.game_count / 2:
                return True
        else:
            if self.played_count == self.game_count:
                return True
        return False

    def match_loop(self):
        """ This method handles the match loop. Each iteration of the
        loop is a single game in the match. When the match is over, it
        returns the scores and wins/draws count as a tuple.
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
