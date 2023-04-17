"""Contains classes of players to supply moves to the checkers game.

The Player class and its subclasses contain the get_next_turn method
that is called by the CheckersMatch object they are associated with.
This supplies the next move in a way that varies for each subclass.

Classes:
    Player: The parent class for all the player classes. Moves are
        supplied manually from command line input.
    RandomPlayer: Chooses moves uniformly randomly from all valid moves.
    Node: Bundles information used as nodes for the search tree created
        for the TreePlayer.
    TreePlayer: This class creates a search tree to find the best moves
        then takes them.
    EasyPlayer, MediumPlayer, HardPlayer: Subclasses of the TreePlayer
        with parameters tuned to make them more or less capable.
"""
# TODO: Make mid and late game based off piece count.

import random


class Player():
    """Gets the next turn from command line input.
    
    This class is intended to be subclassed and the get_next_turn method
    overwritten by other methods to get moves.
    
    Attributes:
        name: A class attribute string to display in the user interface
            to determine the type of player.
        verbose: A boolean; if True, visualizes the board and prints the
        last move at each step.
        gamestate: A Gamestate instance representing the game that the
            Player is playing.
    """

    name = "Manual Player"

    def __init__(self, verbose=False):
        self.gamestate = None
        self.verbose = verbose

    def get_next_turn(self):
        """Passes command line inputted move to the checkers match.
        
        Returns:
            A tuple representing the next move for the checkers match.
        """
        if self.gamestate.invalid_flag:
            print('Invalid last move.')
        elif self.verbose:
            print(self.gamestate.viz_board())
            print('Last move: %s' % (self.gamestate.prev_move,))

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
    """Selects a move at random uniformly from all valid moves.
        
    Attributes:
        See Player class.
    """

    name = "Random Player"

    def get_next_turn(self):
        """Choose a move randomly from all valid moves.
        
        Returns:
            A tuple representing the next chosen move."""
        if self.gamestate.invalid_flag:
            print('Invalid last move.')
        elif self.verbose:
            print(self.gamestate.viz_board())
            print('Last move: %s' % (self.gamestate.prev_move,))

        move_list = self.gamestate.get_valid_moves()
        return move_list[random.randrange(len(move_list))]


class Node():
    """Nodes on the tree used for the tree search player. 
    
    Attributes:
        gamestate: A Gamestate object that represents the gamestate at
            this node
        child_ply: A dictionary containing the next nodes as values and
            the (full) moves to access them as keys.
        terminal: A boolean that indicates whether this is a terminal
            node, i.e. if the game is over in this state.
        score: Evaluation of this node's gamestate.
    """

    def __init__(self, gamestate):
        self.gamestate = gamestate
        self.child_ply = {}
        self.terminal = False
        self.score = 0


class TreePlayer(Player):
    """Creates and scores a search tree then selects the best move.
    
    Attributes:
        parent_node: The node object that is the parent of the tree.
        gamestate: The current gamestate object for the game being
            played. When a new gamestate object is set, the player is
            reset completely as it is assumed a new game is starting.
        cont_move: When playing a multi-part move, the instance records
            the entire move here, as it is fed one part at a time to the
            CheckersMatch instance.
        cont_count: Used to iterate along cont_move.
        verbose: See parent class.
        name: See parent class.
        plys_ini, plys_mid, pls_late: The number of plys to search
            forward at the beginning of the game, the midgame, and the
            late game.
        mid_cutoff, late_cutoff: Ply counts to determine midgame and
            the late game.
        man_score, king_score, victory_score, avg_wt: scoring 
            parameters. See the score_leaf and score_branch methods.
    """

    name = "Tree Player"
    plys_ini = 3
    plys_mid = 5
    plys_late = 8
    mid_cutoff = 50
    late_cutoff = 80
    man_score = 1
    king_score = 3
    victory_score = 40
    avg_wt = 0.1

    def __init__(self, verbose=False):
        """Initializes the tree player.
        
        Args:
            verbose: see parent class.
        """

        self.parent_node = None
        self._gamestate = None
        self.plys = self.plys_ini
        self.cont_move = ()
        self.cont_count = 0
        self.verbose = verbose

    @property
    def gamestate(self):
        return self._gamestate

    @gamestate.setter
    def gamestate(self, new_gamestate):
        """Resets the player completely and assigns the new gamestate.
        
        Args:
            new_gamestate: The new Gamestate instance to be set as the
            gamestate attribute.
            """

        self._gamestate = new_gamestate
        self.parent_node = None
        self.plys = self.plys_ini
        self.cont_move = ()
        self.cont_count = 0

    def score_leaf(self, node):
        """ Scores the end nodes of the current tree.

        Args:
            node: An instance of the Node class to be scored.
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
        """Backpropagates scores on leaves to previous branches.

        Args:
            node: An instance of the Node class to be scored.
            child_scores: A list of the scores of its child nodes.
        """

        if node.gamestate.turn == 1:
            node.score = max(child_scores)
        else:
            node.score = min(child_scores)
        if node.gamestate.ply_count < self.late_cutoff:
            node.score += self.avg_wt * sum(child_scores) / len(child_scores)

    def gen_child_ply(self, node, plys):
        """Generates the next ply (layer) of nodes.

        This method is used recursively to then generate a further ply;
        the plys input stops this process once it reaches required
        depth.

        Args:
            node: An instance of the Node class of which to create the
                next layer.
            plys: An integer tracking how many plys further to go.
        
        Returns:
            A list of scores from the children generated. These are used
            then to score the given node.
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
                        next_gamestate.update(move[ind * 2:(ind+1) * 2])
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
        """Visualize the search tree for debugging purposes.

        Args:
            node: An instance of the node class from which to visualize
                the tree. When first called, pass the parent node of the
                tree to visualize.
            prev_str: A string passed to be built upon as this method
                is used recursively.
        """

        for child in node.child_ply.items():
            print('{}{}: {}'.format(prev_str, child[0], child[1].score))
            self.visualize_tree(child[1], prev_str + '--')

    def get_next_turn(self):
        """Returns the best move found from the search tree.

        Returns:
            A tuple representing the best move found.        
        """

        if self.gamestate.invalid_flag:
            print('Invalid last move.')
        elif self.verbose:
            print(self.gamestate.viz_board())
            print('Last move: %s' % (self.gamestate.prev_move,))

        if not self.cont_move:
            self.cont_count = 0
            # No continuation
            if not self.parent_node:
                # First turn of the game
                self.parent_node = Node(self.gamestate)

            else:
                # Need to update tree based on opponent's last move
                self.parent_node =\
                    self.parent_node.child_ply[self.gamestate.prev_move]
            if self.gamestate.ply_count > self.late_cutoff:
                self.plys = self.plys_late
            elif self.gamestate.ply_count > self.mid_cutoff:
                self.plys = self.plys_mid
            child_scores = self.gen_child_ply(self.parent_node, self.plys)

            # Debug code to visualize tree:
            # self.visualize_tree(self.parent_node, '')

            if self.gamestate.turn == 1:
                best_score = max(child_scores)
            else:
                best_score = min(child_scores)
            best_moves = []
            for child_tuple in self.parent_node.child_ply.items():
                if child_tuple[1].score == best_score:
                    best_moves.append(child_tuple[0])

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
    plys_mid = 3
    plys_late = 4


class HardPlayer(TreePlayer):
    name = "Hard Difficulty"
    plys_ini = 4
    plys_mid = 5
    plys_late = 6
