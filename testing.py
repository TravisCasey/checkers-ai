import unittest

import checkers.game


class TestGame(unittest.TestCase):
    def test_piece_translator(self):
        self.assertEqual(checkers.game.piece_translator(-2), "X")
        self.assertEqual(checkers.game.piece_translator(-1), "x")
        self.assertEqual(checkers.game.piece_translator(0), " ")
        self.assertEqual(checkers.game.piece_translator(1), "o")
        self.assertEqual(checkers.game.piece_translator(2), "O")
        self.assertEqual(checkers.game.piece_translator(7), "error")
        self.assertEqual(checkers.game.piece_translator(-10), "error")


    def test_board_visualization_beginning(self):
        self.assertEqual(checkers.game.visualize_board([ 1,  1,  1,  1,
                                                         1,  1,  1,  1,
                                                         1,  1,  1,  1,
                                                         0,  0,  0,  0,
                                                         0,  0,  0,  0,
                                                        -1, -1, -1, -1,
                                                        -1, -1, -1, -1,
                                                        -1, -1, -1, -1]), 
                                                        "\
| |o| |o| |o| |o|\n\
|o| |o| |o| |o| |\n\
| |o| |o| |o| |o|\n\
| | | | | | | | |\n\
| | | | | | | | |\n\
|x| |x| |x| |x| |\n\
| |x| |x| |x| |x|\n\
|x| |x| |x| |x| |")
         

    def test_board_visualization_midgame(self):
        self.assertEqual(checkers.game.visualize_board([-2,  0,  1,  1,
                                                         0,  0,  0,  0,
                                                         0,  0,  0,  0,
                                                         0,  0,  1,  0,
                                                         0,  0,  0,  0,
                                                         1,  2,  0,  0,
                                                         0,  0,  0, -1,
                                                        -1,  0,  0, 0]), 
                                                        "\
| |X| | | |o| |o|\n\
| | | | | | | | |\n\
| | | | | | | | |\n\
| | | | |o| | | |\n\
| | | | | | | | |\n\
|o| |O| | | | | |\n\
| | | | | | | |x|\n\
|x| | | | | | | |") 
    
    def test_board_visualization_error(self):
        self.assertEqual(checkers.game.visualize_board([0, 2, 1, 4, 5]), "error")
        self.assertEqual(checkers.game.visualize_board(41), "error")
        self.assertEqual(checkers.game.visualize_board([-2,  0,  1,  1,
                                                         0,  0,  0,  0,
                                                         0,  0,  0,  0,
                                                         0,  0,  1,  0,
                                                         0,  0,  3,  0,
                                                         1,  2,  0,  0,
                                                         0,  0,  0, -1,
                                                        -1,  0,  0, 0]), "error")


    def test_is_game_over(self):
        # Needs to be rewritten and moved to game object
        test_state = checkers.game.Gamestate()
        self.assertEqual(test_state.is_game_over(), 0)
        test_state.set_board([    1,  1,  1,  1,
                                  0,  1,  0,  2,
                                  0,  0,  0,  0,
                                  0,  0,  0,  0,
                                  0,  0,  0,  0,
                                  0,  0,  0,  0,
                                  1,  1,  2,  0,
                                  0,  0,  0,  2])
        self.assertEqual(test_state.is_game_over(), 1)
        test_state.set_board([   -2, -2,  0,  0,
                                  0,  0,  0,  0,
                                  0,  0,  0,  0,
                                  0,  0,  0,  0,
                                  0,  0,  0,  0,
                                  0,  0,  0,  0,
                                 -1, -1, -1,  0,
                                  0,  0,  0, -1])
        self.assertEqual(test_state.is_game_over(), -1)
        test_state.set_board([   -2, -2,  0,  0,
                                  0,  0,  0,  0,
                                  0,  0,  0,  0,
                                  0,  0,  1,  0,
                                  0,  0,  0,  0,
                                  0,  0,  0,  0,
                                 -1,  1, -1,  0,
                                  0,  0,  0, -1])
        self.assertEqual(test_state.is_game_over(), 0)


    def test_target_position(self):
        self.assertEqual(checkers.game.target_position(0, 2), 4)
        self.assertEqual(checkers.game.target_position(17, 0), 14)
        self.assertEqual(checkers.game.target_position(9, 1), 5)
        self.assertEqual(checkers.game.target_position(4, 3), 8)
        self.assertEqual(checkers.game.target_position(6, 1), 1)
        self.assertEqual(checkers.game.target_position(22, 2), 25)
        self.assertEqual(checkers.game.target_position(31, 2), -1)
        self.assertEqual(checkers.game.target_position(2, 1), -1)
        self.assertEqual(checkers.game.target_position(11, 3), -1)
        self.assertEqual(checkers.game.target_position(20, 2), -1)
        self.assertEqual(checkers.game.target_position(12, 1), -1)
        self.assertEqual(checkers.game.target_position(-3, 2), -1)
        self.assertEqual(checkers.game.target_position(12, 6), -1)
        
        
    def test_can_jump(self):
        test_state = checkers.game.Gamestate()
        test_state.set_board([  0,  1,  1,  1,      # | | | |o| |o| |o|
                                0,  1,  0,  2,      # | | |o| | | |O| |
                                0, -1, -1,  0,      # | | | |x| |x| | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0, -1, -1, -1,      # | | | |x| |x| |x|
                                0,  0,  1,  0,      # | | | | |o| | | |
                               -1, -1, -2,  0,      # | |x| |x| |X| | |
                                0,  0,  0,  2])     # | | | | | | |O| |
        self.assertEqual(test_state.piece_can_jump(0, 0), False)
        self.assertEqual(test_state.piece_can_jump(0, 2), False)
        self.assertEqual(test_state.piece_can_jump(1, 1), False)
        self.assertEqual(test_state.piece_can_jump(1, 2), False)
        self.assertEqual(test_state.piece_can_jump(1, 3), False)
        self.assertEqual(test_state.piece_can_jump(5, 2), False)
        self.assertEqual(test_state.piece_can_jump(5, 3), True)
        self.assertEqual(test_state.piece_can_jump(7, 0), False)
        self.assertEqual(test_state.piece_can_jump(7, 2), True)
        self.assertEqual(test_state.piece_can_jump(9, 1), True)
        self.assertEqual(test_state.piece_can_jump(10, 1), False)
        self.assertEqual(test_state.piece_can_jump(17, 0), False)
        self.assertEqual(test_state.piece_can_jump(17, 1), False)
        self.assertEqual(test_state.piece_can_jump(22, 0), False)
        self.assertEqual(test_state.piece_can_jump(22, 1), False)
        self.assertEqual(test_state.piece_can_jump(22, 2), True)
        self.assertEqual(test_state.piece_can_jump(22, 3), False)
        self.assertEqual(test_state.piece_can_jump(26, 1), False)
        self.assertEqual(test_state.piece_can_jump(30, 1), False)
        self.assertEqual(test_state.piece_can_jump(31, 0), False)
        self.assertEqual(test_state.piece_can_jump(33, 2), False)
        self.assertEqual(test_state.piece_can_jump(5, -2), False)


    def test_is_valid(self):
        test_state = checkers.game.Gamestate()
        test_state.set_board([ -2,  1,  1,  0,      # | |X| |o| |o| | |
                                0,  0,  0,  2,      # | | | | | | |O| |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0, -1,  0,  0,      # | | |x| | | | | |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0,  0,  1,  0,      # | | | | |o| | | |
                               -1,  0,  0,  0,      # | |x| | | | | | |
                                0,  0,  0,  2])     # | | | | | | |O| |
        test_state.set_turn(-1)
        self.assertEqual(test_state.is_valid(0, 0), False)
        self.assertEqual(test_state.is_valid(0, 2), True)
        self.assertEqual(test_state.is_valid(0, 3), True)
        test_state.set_turn(1)
        self.assertEqual(test_state.is_valid(1, 2), True)
        self.assertEqual(test_state.is_valid(1, 3), True)
        self.assertEqual(test_state.is_valid(2, 3), False)
        test_state.set_turn(-1)
        self.assertEqual(test_state.is_valid(1, 3), False)
        self.assertEqual(test_state.is_valid(3, 3), False)
        self.assertEqual(test_state.is_valid(-3, 3), False)
        self.assertEqual(test_state.is_valid(2, 5), False)
        self.assertEqual(test_state.is_valid(13, 1), True)
        test_state.set_continuation(24)
        self.assertEqual(test_state.is_valid(13, 1), False)
        self.assertEqual(test_state.is_valid(24, 1), True)
        test_state.set_board([ -2,  1,  1,  0,      # | |X| |o| |o| | |
                                0,  1,  0,  2,      # | | |o| | | |O| |
                                0,  0,  0,  0,      # | | | | | | | | |
                                0, -1,  0,  0,      # | | |x| | | | | |
                                0,  0,  -2,  0,     # | | | | | |X| | |
                                0,  0,  1,  0,      # | | | | |o| | | |
                               -1, -1,  0,  0,      # | |x| |x| | | | |
                                0,  0,  0,  2])     # | | | | | | |O| |
        test_state.set_continuation(-1)
        self.assertEqual(test_state.is_valid(0, 2), False)
        self.assertEqual(test_state.is_valid(0, 3), True)
        self.assertEqual(test_state.is_valid(18, 2), False)
        self.assertEqual(test_state.is_valid(25, 0), False)
        test_state.set_turn(1)
        self.assertEqual(test_state.is_valid(22, 2), True)
        self.assertEqual(test_state.is_valid(22, 1), False)

if __name__ == "__main__":
    unittest.main()