import unittest
import checkers
import torch
import matplotlib.pyplot as plt


class TestGame(unittest.TestCase):
    def test_target_pos(self):
        self.assertEqual(checkers.game.target_pos((0, 2)), 4)
        self.assertEqual(checkers.game.target_pos((17, 0)), 14)
        self.assertEqual(checkers.game.target_pos((9, 1)), 5)
        self.assertEqual(checkers.game.target_pos((4, 3)), 8)
        self.assertEqual(checkers.game.target_pos((6, 1)), 1)
        self.assertEqual(checkers.game.target_pos((22, 2)), 25)
        self.assertEqual(checkers.game.target_pos((31, 2)), None)
        self.assertEqual(checkers.game.target_pos((2, 1)), None)
        self.assertEqual(checkers.game.target_pos((11, 3)), None)
        self.assertEqual(checkers.game.target_pos((20, 2)), None)
        self.assertEqual(checkers.game.target_pos((12, 1)), None)
        with self.assertRaises(TypeError):
            checkers.game.target_pos(('three', 2))
            checkers.game.target_pos(3, None)
        with self.assertRaises(ValueError):
            checkers.game.target_pos((-2, 2))
            checkers.game.target_pos((3, 14))

    def test_piece_dicts(self):
        test_gamestate = checkers.game.Gamestate()
        self.assertEqual(test_gamestate.piece_dirs[1], (2, 3))
        self.assertEqual(test_gamestate.piece_dirs[2], (0, 1, 2, 3))
        self.assertEqual(test_gamestate.piece_dirs[-1], (0, 1))
        self.assertEqual(test_gamestate.piece_dirs[-2], (0, 1, 2, 3))
        self.assertEqual(test_gamestate.piece_dirs[0], ())
        self.assertEqual(test_gamestate.team_pieces[1], (1, 2))
        self.assertEqual(test_gamestate.team_pieces[-1], (-1, -2))
        self.assertEqual(test_gamestate.opp_pieces[1], (-1, -2))
        self.assertEqual(test_gamestate.opp_pieces[2], (-1, -2))
        self.assertEqual(test_gamestate.opp_pieces[-1], (1, 2))
        self.assertEqual(test_gamestate.opp_pieces[-2], (1, 2))
        self.assertEqual(test_gamestate.piece_reps[1], 'o')
        self.assertEqual(test_gamestate.piece_reps[2], 'O')
        self.assertEqual(test_gamestate.piece_reps[-1], 'x')
        self.assertEqual(test_gamestate.piece_reps[-2], 'X')
        self.assertEqual(test_gamestate.piece_reps[0], ' ')

    def test_viz_board(self):
        test_gamestate = checkers.game.Gamestate()
        test_gamestate.board = [1,  1,  1,  1,
                                1,  1,  1,  1,
                                1,  1,  1,  1,
                                0,  0,  0,  0,
                                0,  0,  0,  0,
                                -1, -1, -1, -1,
                                -1, -1, -1, -1,
                                -1, -1, -1, -1]
        self.assertEqual(test_gamestate.viz_board(), '\
| |o| |o| |o| |o|\n\
|o| |o| |o| |o| |\n\
| |o| |o| |o| |o|\n\
| | | | | | | | |\n\
| | | | | | | | |\n\
|x| |x| |x| |x| |\n\
| |x| |x| |x| |x|\n\
|x| |x| |x| |x| |\n\
Team 1 turn.')
        test_gamestate.board = [-2,  0,  1,  1,
                                0,  0,  0,  0,
                                0,  0,  0,  0,
                                0,  0,  1,  0,
                                0,  0,  0,  0,
                                1,  2,  0,  0,
                                0,  0,  0, -1,
                                -1,  0,  0, 0]
        test_gamestate.turn = -1
        self.assertEqual(test_gamestate.viz_board(), '\
| |X| | | |o| |o|\n\
| | | | | | | | |\n\
| | | | | | | | |\n\
| | | | |o| | | |\n\
| | | | | | | | |\n\
|o| |O| | | | | |\n\
| | | | | | | |x|\n\
|x| | | | | | | |\n\
Team 2 turn.')

    def test_is_jump(self):
        test_state = checkers.game.Gamestate()
        test_state.board = [0,  1,  1,  1,      # | | | |o| |o| |o|
                            0,  1,  0,  2,      # | | |o| | | |O| |
                            0, -1, -1,  0,      # | | | |x| |x| | |
                            0,  0,  0,  0,      # | | | | | | | | |
                            0, -1, -1, -1,      # | | | |x| |x| |x|
                            0,  0,  1,  0,      # | | | | |o| | | |
                            -1, -1, -2,  0,     # | |x| |x| |X| | |
                            0,  0,  0,  2]      # | | | | | | |O| |
        self.assertEqual(test_state.is_jump((0, 0)), False)
        self.assertEqual(test_state.is_jump((0, 2)), False)
        self.assertEqual(test_state.is_jump((1, 1)), False)
        self.assertEqual(test_state.is_jump((1, 2)), False)
        self.assertEqual(test_state.is_jump((1, 3)), False)
        self.assertEqual(test_state.is_jump((5, 2)), False)
        self.assertEqual(test_state.is_jump((5, 3)), True)
        self.assertEqual(test_state.is_jump((7, 0)), False)
        self.assertEqual(test_state.is_jump((7, 2)), True)
        self.assertEqual(test_state.is_jump((9, 1)), True)
        self.assertEqual(test_state.is_jump((10, 1)), False)
        self.assertEqual(test_state.is_jump((17, 0)), False)
        self.assertEqual(test_state.is_jump((17, 1)), False)
        self.assertEqual(test_state.is_jump((22, 0)), False)
        self.assertEqual(test_state.is_jump((22, 1)), False)
        self.assertEqual(test_state.is_jump((22, 2)), True)
        self.assertEqual(test_state.is_jump((22, 3)), False)
        self.assertEqual(test_state.is_jump((26, 1)), False)
        self.assertEqual(test_state.is_jump((30, 1)), False)
        self.assertEqual(test_state.is_jump((31, 0)), False)
        with self.assertRaises(TypeError):
            test_state.is_jump(([41], 2))
            test_state.is_jump((5, None))
        with self.assertRaises(ValueError):
            test_state.is_jump((33, 2))
            test_state.is_jump((5, -2))
        test_state.board = [0,  0,  1,  1,       # | | | | | |o| |o|
                            0, -1,  0,  0,       # | | |x| | | | | |
                            1,  0,  0,  1,       # | |o| | | | | |o|
                            0,  0,  0,  0,       # | | | | | | | | |
                            0, -1,  1,  0,       # | | | |x| |o| | |
                            -1,  0, -1,  0,      # |x| | | |x| | | |
                            -1,  0,  0,  1,      # | |x| | | | | |o|
                            -1, -1, -1,  0]      # |x| |x| |x| | | |
        self.assertEqual(test_state.is_jump((5, 2)), False)
        self.assertEqual(test_state.can_jump(0), False)
        self.assertEqual(test_state.can_jump(2), False)
        self.assertEqual(test_state.can_jump(5), False)
        self.assertEqual(test_state.can_jump(8), False)
        self.assertEqual(test_state.can_jump(18), True)

    def test_is_valid(self):
        test_state = checkers.game.Gamestate()
        test_state.board = [-2,  1,  1,  0,      # | |X| |o| |o| | |
                            0,  0,  0,  2,       # | | | | | | |O| |
                            0,  0,  0,  0,       # | | | | | | | | |
                            0, -1,  0,  0,       # | | |x| | | | | |
                            0,  0,  0,  0,       # | | | | | | | | |
                            0,  0,  1,  0,       # | | | | |o| | | |
                            -1,  0,  0,  0,      # | |x| | | | | | |
                            0,  0,  0,  2]       # | | | | | | |O| |
        test_state.turn = -1
        self.assertEqual(test_state.is_valid((0, 0)), False)
        self.assertEqual(test_state.is_valid((0, 2)), True)
        self.assertEqual(test_state.is_valid((0, 3)), True)
        test_state.turn = 1
        self.assertEqual(test_state.is_valid((1, 2)), True)
        self.assertEqual(test_state.is_valid((1, 3)), True)
        self.assertEqual(test_state.is_valid((2, 3)), False)
        test_state.turn = -1
        self.assertEqual(test_state.is_valid((1, 3)), False)
        self.assertEqual(test_state.is_valid((3, 3)), False)
        with self.assertRaises(TypeError):
            test_state.is_valid(([13, 1], 1))
            test_state.is_valid((13, "one"))
        with self.assertRaises(ValueError):
            test_state.is_valid((-3, 3))
            test_state.is_valid((2, 5))
        self.assertEqual(test_state.is_valid((13, 1)), True)
        test_state.cont = 24
        self.assertEqual(test_state.is_valid((13, 1)), False)
        self.assertEqual(test_state.is_valid((24, 1)), True)
        test_state.board = [-2,  1,  1,  0,      # | |X| |o| |o| | |
                            0,  1,  0,  2,       # | | |o| | | |O| |
                            0,  0,  0,  0,       # | | | | | | | | |
                            0, -1,  0,  0,       # | | |x| | | | | |
                            0,  0, -2,  0,       # | | | | | |X| | |
                            0,  0,  1,  0,       # | | | | |o| | | |
                            -1, -1,  0,  0,      # | |x| |x| | | | |
                            0,  0,  0,  2]       # | | | | | | |O| |
        test_state.cont = None
        self.assertEqual(test_state.is_valid((0, 2)), False)
        self.assertEqual(test_state.is_valid((0, 3)), True)
        self.assertEqual(test_state.is_valid((18, 2)), False)
        self.assertEqual(test_state.is_valid((25, 0)), False)
        test_state.turn = 1
        self.assertEqual(test_state.is_valid((22, 2)), True)
        self.assertEqual(test_state.is_valid((22, 1)), False)

    def test_get_valid_moves(self):
        test_state = checkers.game.Gamestate()
        self.assertEqual(test_state.get_valid_moves(), [(8, 2), (8, 3),
                                                        (9, 2), (9, 3),
                                                        (10, 2), (10, 3),
                                                        (11, 2)])
        test_state.board = [-2,  1,  1,  0,      # | |X| |o| |o| | |
                            0,  1,  0,  2,       # | | |o| | | |O| |
                            0,  0,  0,  0,       # | | | | | | | | |
                            0, -1,  0,  0,       # | | |x| | | | | |
                            0,  0, -2,  0,       # | | | | | |X| | |
                            0,  0,  1,  0,       # | | | | |o| | | |
                            -1, -1,  0,  0,      # | |x| |x| | | | |
                            0,  0,  0,  2]       # | | | | | | |O| |
        test_state.turn = -1
        self.assertEqual(test_state.get_valid_moves(), [(0, 3)])

    def test_update(self):
        test_gamestate = checkers.game.Gamestate()
        self.assertEqual(test_gamestate.update((10, 3)), None)
        self.assertEqual(test_gamestate.update((22, 0)), None)
        self.assertEqual(test_gamestate.update((15, 2)), None)
        self.assertEqual(test_gamestate.update((25, 0)), None)
        self.assertEqual(test_gamestate.update((9, 2)), None)
        self.assertEqual(test_gamestate.update((26, 1)), None)
        self.assertEqual(test_gamestate.update((7, 2)), None)
        self.assertEqual(test_gamestate.update((18, 0)), None)
        self.assertEqual(test_gamestate.update((11, 2)), None)
        self.assertEqual(test_gamestate.update((18, 2)), None)
        self.assertEqual(test_gamestate.update((29, 0)), None)
        self.assertEqual(test_gamestate.update((8, 2)), None)
        self.assertEqual(test_gamestate.update((23, 1)), None)
        self.assertEqual(test_gamestate.update((10, 3)), None)
        self.assertEqual(test_gamestate.update((18, 0)), None)
        self.assertEqual(test_gamestate.update((4, 3)), None)
        self.assertEqual(test_gamestate.update((31, 1)), None)
        self.assertEqual(test_gamestate.update((3, 2)), None)
        self.assertEqual(test_gamestate.update((22, 1)), None)
        self.assertEqual(test_gamestate.update((13, 3)), None)
        self.assertEqual(test_gamestate.update((22, 3)), None)
        self.assertEqual(test_gamestate.update((30, 0)), None)
        self.assertEqual(test_gamestate.update((31, 1)), None)
        self.assertEqual(test_gamestate.update((20, 0)), None)
        self.assertEqual(test_gamestate.update((22, 3)), None)

    def test_is_game_over(self):
        test_gamestate = checkers.game.Gamestate()
        self.assertEqual(test_gamestate.is_game_over(), 2)
        test_gamestate.plys_since_capture = 80
        self.assertEqual(test_gamestate.is_game_over(), 0)
        test_gamestate.board = [0,  1,  1,  0,      # | | | |o| |o| | |
                                0,  1,  0,  2,      # | | |o| | | |O| |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0,  0,  1,  0,      # | | | | |o| | | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0,  0,  0,  2]      # | | | | | | |O| |
        test_gamestate.plys_since_capture = 0
        test_gamestate.turn = -1
        self.assertEqual(test_gamestate.is_game_over(), 1)
        test_gamestate.board = [0,  0,  0,  0,      # | | | | | | | | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0,  1,  0,  0,      # | | |o| | | | | |
                                -1, -1,  0,  0,     # | |x| |x| | | | |
                                -1,  0, -1,  0]     # |x| | | |x| | | |
        test_gamestate.turn = 1
        self.assertEqual(test_gamestate.is_game_over(), -1)

    def test_get_full_moves(self):
        test_gamestate = checkers.game.Gamestate()
        test_gamestate.board = [0,  0,  0,  0,      # | | | | | | | | |
                                1,  0,  0,  0,      # |o| | | | | | | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0,  1,  1,  0,      # | | |o| |o| | | |
                                0, -1, -1,  0,      # | | | |x| |x| | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                -1, -1,  0,  0,     # | |x| |x| | | | |
                                0,  0,  0,  0]      # | | | | | | | | |
        self.assertEqual(test_gamestate.get_full_moves(), [(13, 3, 22, 2),
                                                           (14, 2, 21, 2),
                                                           (14, 2, 21, 3),
                                                           (14, 3)])
        test_gamestate.cont = 13
        self.assertEqual(test_gamestate.get_full_moves(), [(13, 3, 22, 2)])
        test_gamestate.cont = None
        test_gamestate.turn = -1
        self.assertEqual(test_gamestate.get_full_moves(), [(17, 0),
                                                           (17, 1),
                                                           (18, 1)])

def plot_loss(prev_points, new_points, final=False):
    ALPHA = 0.002
    plt.clf()
    plt.xlabel('Episodes')
    plt.ylabel('Loss')
    if not final:
        plt.title('Training')
        for point in new_points:
            if not prev_points:
                prev_points.append(point)
            else:
                prev_points.append(ALPHA * point + (1 - ALPHA) * prev_points[-1])
        if len(prev_points) >= 10000:
            plt.xlim(left=len(prev_points) - 10000, right=len(prev_points))
        plt.plot(prev_points)
        plt.pause(1)
        plt.show()
        return prev_points
    else:
        plt.title('Final Results')
        plt.xlim(left=0, right=len(prev_points))
        plt.plot(prev_points)
        plt.show()


if __name__ == "__main__":
    # unittest.main()
    plot_list = [i for i in range(5000)]
    new_list = [i for i in range(5000)]
    plot_loss(plot_list, new_list, True)
