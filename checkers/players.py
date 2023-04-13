import random
""" This module contains the Player class, and various subclasses.
These subclasses make up the various ways moves are chosen.
"""
# TODO: Make mid and late game based off piece count.


class Player():
    """ The Player class gets the next turn from manual input from the
    player. It is intended to be subclassed by other methods to input
    turns. Its attributes are:
    - gamestate: A gamestate object representing the game it is playing.
    - team: Indicates which team the player is playing. Values 1, -1."""

    name = "Manual Player"

    def __init__(self, team):
        self.gamestate = None
        self.team = team

    def get_next_turn(self, opp_move):
        """ This method accepts command line move input from the player
        and returns it as a tuple."""
        print(self.gamestate.viz_board())
        print('Last move: %s' % (opp_move,))

        while True:
            try:
                pos = int(input('Position: '))
            except ValueError:
                print('Enter a position integer between 0 and 31.')
                continue
            if pos not in range(32):
                print('Enter a position integer between 0 and 31')
                continue
            else:
                break

        while True:
            try:
                dir = int(input('Direction: '))
            except ValueError:
                print('Enter a direction integer between 0 and 3.')
                continue
            if dir not in range(4):
                print('Enter a direction integer between 0 and 3')
                continue
            else:
                break

        return (pos, dir)


class RandomPlayer(Player):
    """ This subclass selects a move at random from all valid moves."""

    name = "Random Player"

    def get_next_turn(self, opp_move):
        print(self.gamestate.viz_board())
        move_list = self.gamestate.get_valid_moves()
        return move_list[random.randrange(len(move_list))]


class Node():
    """ Instances of this class are nodes on the tree used for
    the tree search player. The attributes are:
    - gamestate: A Gamestate object that represents the gamestate at
    this node
    - child_ply: A dictionary containing the next nodes as values and
    the moves to access them as keys.
    - terminal: A boolean that indicates whether this is a terminal
    node, i.e. if the game is over in this state.
    - score: Evaluation of this node's gamestate.
    """

    def __init__(self, gamestate):
        self.gamestate = gamestate
        self.child_ply = {}
        self.terminal = False
        self.score = 0


class TreePlayer(Player):
    """ This subclass creates a tree from the given gamestate and
    searches ahead to find optimal moves. The class attributes are the
    name and parameters to tweak the search and scoring.
    The instance attributes are:
    - parent_node: The node object that is the parent of the tree.
    - gamestate: The current gamestate object for the game being played.
    - team: The team the instance plays for.
    - cont_move: When playing a multi-part move, the instance records
    the entire move here, as it is fed one part at a time to the
    CheckersMatch object.
    - cont_count: Used to iterate along cont_move.
    """

    name = "Tree Player"
    plys_ini = 3
    plys_mid = 5
    plys_late = 8
    mid_cutoff = 40
    late_cutoff = 60
    man_score = 1
    king_score = 3
    victory_score = 40
    avg_wt = 0.1

    def __init__(self, team):
        self.parent_node = None
        self._gamestate = None
        self.team = team
        self.plys = self.plys_ini
        self.cont_move = ()
        self.cont_count = 0

    @property
    def gamestate(self):
        return self._gamestate

    @gamestate.setter
    def gamestate(self, new_gamestate):
        """ Resets the player completely."""
        self._gamestate = new_gamestate
        self.parent_node = None
        self.plys = self.plys_ini
        self.cont_move = ()
        self.cont_count = 0

    def score_leaf(self, node):
        """ This method scores the ends of the current tree, which can
        be backpropagated to score previous nodes.
        """
        score = 0
        for piece in node.gamestate.board:
            match piece:
                case -2:
                    score -= self.king_score
                case -1:
                    score -= self.man_score
                case 1:
                    score += self.man_score
                case 2:
                    score += self.king_score
        node.score = score

    def score_branch(self, node, child_scores):
        """ This method contains the algorithm for backpropagating
        scores on leaves to previous branches.
        """
        if self.team == 1:
            node.score = min(child_scores)
        else:
            node.score = max(child_scores)
        if node.gamestate.ply_count < self.late_cutoff:
            node.score += self.avg_wt * sum(child_scores) / len(child_scores)

    def gen_child_ply(self, node, plys):
        """This method takes in a node and generates the next ply.
        This method is used recursively to then generate a further ply;
        the plys input stops this process once it reaches required
        depth. It then returns the scores of its child nodes in a list.
        """
        score_list = []
        if not node.child_ply:
            # Ply has not been generated
            move_list = node.gamestate.get_full_moves()
            if not move_list:
                node.terminal = True
                score_list = [-1 * node.gamestate.turn * self.victory_score]
            else:
                for move in move_list:
                    next_gamestate = node.gamestate.copy()
                    for ind in range(len(move) // 2):
                        next_gamestate.update(move[ind * 2], move[ind*2 + 1])
                    child = Node(next_gamestate)
                    node.child_ply[move] = child
                    if plys == 1:
                        # child is a leaf
                        self.score_leaf(child)
                    else:
                        # next_node is a branch
                        child_scores = self.gen_child_ply(child, plys - 1)
                        self.score_branch(child, child_scores)
                    score_list.append(child.score)
        else:
            # Ply has previously been generated
            for child in node.child_ply.values():
                if not child.terminal:
                    # Need to update non-terminal nodes
                    child_scores = self.gen_child_ply(child, plys - 1)
                    self.score_branch(child, child_scores)
                score_list.append(child.score)
        return score_list

    def visualize_tree(self, node, prev_str):
        """This method is used to visualize the search tree, largely
        for debugging purposes.
        """
        for child in node.child_ply.items():
            print('{}{}: {}'.format(prev_str, child[0], child[1].score))
            self.visualize_tree(child[1], prev_str + '--')

    def get_next_turn(self, opp_move):
        print(self.gamestate.viz_board())
        if not self.cont_move:
            self.cont_count = 0
            # No continuation
            if not self.parent_node:
                # First turn of the game
                self.parent_node = Node(self.gamestate)
            else:
                # Need to update tree based on opponent's last move
                self.parent_node = self.parent_node.child_ply[opp_move]
            if self.gamestate.ply_count > self.late_cutoff:
                self.plys = self.plys_late
            elif self.gamestate.ply_count > self.mid_cutoff:
                self.plys = self.plys_mid
            child_scores = self.gen_child_ply(self.parent_node, self.plys)

            # Debug code to visualize tree
            # self.visualize_tree(self.parent_node, '')

            if self.team == 1:
                best_score = max(child_scores)
            else:
                best_score = min(child_scores)
            best_moves = []
            for child_tuple in self.parent_node.child_ply.items():
                if child_tuple[1].score == best_score:
                    best_moves.append(child_tuple[0])

            # Randomly choose from best_moves
            chosen_move = best_moves[random.randrange(len(best_moves))]

            if len(chosen_move) > 2:
                # Continuation
                self.cont_move = chosen_move
                return self.cont_move[self.cont_count*2:(self.cont_count+1)*2]
            else:
                self.parent_node = self.parent_node.child_ply[chosen_move]
                return chosen_move
        else:
            # Continuation
            self.cont_count += 1
            if (self.cont_count+1) * 2 == len(self.cont_move):
                # Last iteration on this move
                self.parent_node = self.parent_node.child_ply[self.cont_move]
                move_holder = self.cont_move[self.cont_count*2:]
                self.cont_move = ()
                return move_holder
            else:
                # Iterate again
                return self.cont_move[self.cont_count*2:(self.cont_count+1)*2]


class EasyPlayer(TreePlayer):
    name = "Easy Difficulty"
    plys_ini = 2
    plys_mid = 2
    plys_late = 3


class MediumPlayer(TreePlayer):
    name = "Medium Difficulty"
    plys_ini = 3
    plys_mid = 4
    plys_late = 5


class HardPlayer(TreePlayer):
    name = "Hard Difficulty"
    plys_ini = 4
    plys_mid = 5
    plys_late = 6
