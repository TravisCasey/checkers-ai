import unittest
import checkers


class TestGame(unittest.TestCase):
    def test_piece_translator(self):
        self.assertEqual(checkers.game.piece_translator(-2), "X")
        self.assertEqual(checkers.game.piece_translator(-1), "x")
        self.assertEqual(checkers.game.piece_translator(0), " ")
        self.assertEqual(checkers.game.piece_translator(1), "o")
        self.assertEqual(checkers.game.piece_translator(2), "O")
        with self.assertRaises(TypeError):
            checkers.game.piece_translator('two')
        with self.assertRaises(ValueError):
            checkers.game.piece_translator(7)
            checkers.game.piece_translator(-2)

    def test_board_visualization(self):
        self.assertEqual(checkers.game.visualize_board([ 1,  1,  1,  1,
                                                         1,  1,  1,  1,
                                                         1,  1,  1,  1,
                                                         0,  0,  0,  0,
                                                         0,  0,  0,  0,
                                                        -1, -1, -1, -1,
                                                        -1, -1, -1, -1,
                                                        -1, -1, -1, -1]), 
                                                        '\
| |o| |o| |o| |o|\n\
|o| |o| |o| |o| |\n\
| |o| |o| |o| |o|\n\
| | | | | | | | |\n\
| | | | | | | | |\n\
|x| |x| |x| |x| |\n\
| |x| |x| |x| |x|\n\
|x| |x| |x| |x| |')
        self.assertEqual(checkers.game.visualize_board([-2,  0,  1,  1,
                                                         0,  0,  0,  0,
                                                         0,  0,  0,  0,
                                                         0,  0,  1,  0,
                                                         0,  0,  0,  0,
                                                         1,  2,  0,  0,
                                                         0,  0,  0, -1,
                                                        -1,  0,  0, 0]), 
                                                        '\
| |X| | | |o| |o|\n\
| | | | | | | | |\n\
| | | | | | | | |\n\
| | | | |o| | | |\n\
| | | | | | | | |\n\
|o| |O| | | | | |\n\
| | | | | | | |x|\n\
|x| | | | | | | |') 
        with self.assertRaises(TypeError):
            checkers.game.visualize_board(41)
            checkers.game.visualize_board([0, 2, 1, 4, 5])
        with self.assertRaises(ValueError):
            checkers.game.visualize_board([-2,  0,  1,  1,
                                            0,  0,  0,  0,
                                            0,  0,  0,  0,
                                            0,  0,  1,  0,
                                            0,  0,  3,  0,
                                            1,  2,  0,  0,
                                            0,  0,  0, -1,
                                           -1,  0,  0,  0])

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
        with self.assertRaises(TypeError):
            checkers.game.target_position('three', 2)
            checkers.game.target_position(3, None)
        with self.assertRaises(ValueError):
            checkers.game.target_position(-2, 2)
            checkers.game.target_position(3, 14)        
        
    def test_can_jump(self):
        test_state = checkers.game.Gamestate()
        test_state.board = [ 0,  1,  1,  1,      # | | | |o| |o| |o|
                             0,  1,  0,  2,      # | | |o| | | |O| |
                             0, -1, -1,  0,      # | | | |x| |x| | |
                             0,  0,  0,  0,      # | | | | | | | | |
                             0, -1, -1, -1,      # | | | |x| |x| |x|
                             0,  0,  1,  0,      # | | | | |o| | | |
                            -1, -1, -2,  0,      # | |x| |x| |X| | |
                             0,  0,  0,  2]      # | | | | | | |O| |
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
        with self.assertRaises(TypeError):
            test_state.piece_can_jump([41], 2)
            test_state.piece_can_jump(5, None)
        with self.assertRaises(ValueError):
            test_state.piece_can_jump(33, 2)
            test_state.piece_can_jump(5, -2)
        test_state.board = [ 0,  0,  1,  1,      # | | | | | |o| |o|
                             0, -1,  0,  0,      # | | |x| | | | | |
                             1,  0,  0,  1,      # | |o| | | | | |o|
                             0,  0,  0,  0,      # | | | | | | | | |
                             0, -1,  0,  0,      # | | | |x| | | | |
                            -1,  0, -1,  0,      # |x| | | |x| | | |
                            -1,  0,  0,  1,      # | |x| | | | | |o|
                            -1, -1, -1,  0]      # |x| |x| |x| | | |
        self.assertEqual(test_state.piece_can_jump(5, 2), False)


    def test_is_valid(self):
        test_state = checkers.game.Gamestate()
        test_state.board = [-2,  1,  1,  0,      # | |X| |o| |o| | |
                             0,  0,  0,  2,      # | | | | | | |O| |
                             0,  0,  0,  0,      # | | | | | | | | |
                             0, -1,  0,  0,      # | | |x| | | | | |
                             0,  0,  0,  0,      # | | | | | | | | |
                             0,  0,  1,  0,      # | | | | |o| | | |
                            -1,  0,  0,  0,      # | |x| | | | | | |
                             0,  0,  0,  2]      # | | | | | | |O| |
        test_state.turn = -1
        self.assertEqual(test_state.is_valid(0, 0), False)
        self.assertEqual(test_state.is_valid(0, 2), True)
        self.assertEqual(test_state.is_valid(0, 3), True)
        test_state.turn = 1
        self.assertEqual(test_state.is_valid(1, 2), True)
        self.assertEqual(test_state.is_valid(1, 3), True)
        self.assertEqual(test_state.is_valid(2, 3), False)
        test_state.turn = -1
        self.assertEqual(test_state.is_valid(1, 3), False)
        self.assertEqual(test_state.is_valid(3, 3), False)
        with self.assertRaises(TypeError):
            test_state.is_valid([13, 1], 1)
            test_state.is_valid(13, "one")
        with self.assertRaises(ValueError):
            test_state.is_valid(-3, 3)
            test_state.is_valid(2, 5)
        self.assertEqual(test_state.is_valid(13, 1), True)
        test_state.continuation = 24
        self.assertEqual(test_state.is_valid(13, 1), False)
        self.assertEqual(test_state.is_valid(24, 1), True)
        test_state.board = [-2,  1,  1,  0,      # | |X| |o| |o| | |
                             0,  1,  0,  2,      # | | |o| | | |O| |
                             0,  0,  0,  0,      # | | | | | | | | |
                             0, -1,  0,  0,      # | | |x| | | | | |
                             0,  0, -2,  0,      # | | | | | |X| | |
                             0,  0,  1,  0,      # | | | | |o| | | |
                            -1, -1,  0,  0,      # | |x| |x| | | | |
                             0,  0,  0,  2]      # | | | | | | |O| |
        test_state.continuation = -1
        self.assertEqual(test_state.is_valid(0, 2), False)
        self.assertEqual(test_state.is_valid(0, 3), True)
        self.assertEqual(test_state.is_valid(18, 2), False)
        self.assertEqual(test_state.is_valid(25, 0), False)
        test_state.turn = 1
        self.assertEqual(test_state.is_valid(22, 2), True)
        self.assertEqual(test_state.is_valid(22, 1), False)
    
    def test_get_valid_moves(self):
        test_state = checkers.game.Gamestate()
        self.assertEqual(test_state.get_valid_moves(), [[8, 2], [8, 3], [9, 2], [9, 3], [10, 2], [10, 3], [11, 2]])
        test_state.board = [-2,  1,  1,  0,      # | |X| |o| |o| | |
                             0,  1,  0,  2,      # | | |o| | | |O| |
                             0,  0,  0,  0,      # | | | | | | | | |
                             0, -1,  0,  0,      # | | |x| | | | | |
                             0,  0, -2,  0,      # | | | | | |X| | |
                             0,  0,  1,  0,      # | | | | |o| | | |
                            -1, -1,  0,  0,      # | |x| |x| | | | |
                             0,  0,  0,  2]      # | | | | | | |O| |
        test_state.turn = -1
        self.assertEqual(test_state.get_valid_moves(), [[0, 3]])

    def test_update_gamestate(self):
        test_match = checkers.game.CheckersMatch()
        self.assertEqual(test_match.update_gamestate(10, 3), 1)
        self.assertEqual(test_match.update_gamestate(22, 0), 1)
        self.assertEqual(test_match.update_gamestate(22, 0), 0)
        self.assertEqual(test_match.update_gamestate(15, 3), 0)
        self.assertEqual(test_match.update_gamestate(15, 2), 1)
        self.assertEqual(test_match.update_gamestate(21, 0), 0)
        self.assertEqual(test_match.update_gamestate(-2, 3), 0)
        self.assertEqual(test_match.update_gamestate(-2, 5), 0)
        self.assertEqual(test_match.update_gamestate(25, 0), 1)
        self.assertEqual(test_match.update_gamestate(9, 2), 1)
        self.assertEqual(test_match.update_gamestate(26, 1), 1)
        self.assertEqual(test_match.update_gamestate(7, 2), 1)
        self.assertEqual(test_match.update_gamestate(18, 0), 1)
        self.assertEqual(test_match.update_gamestate(10, 2), 0)
        self.assertEqual(test_match.update_gamestate(11, 2), 2)
        self.assertEqual(test_match.update_gamestate(20, 0), 0)
        self.assertEqual(test_match.update_gamestate(18, 2), 1)
        self.assertEqual(test_match.update_gamestate(29, 0), 1)
        self.assertEqual(test_match.update_gamestate(8, 2), 1)
        self.assertEqual(test_match.get_turn_count(1), 6)
        self.assertEqual(test_match.get_turn_count(-1), 5)
        self.assertEqual(test_match.team_1_moves, [[10, 3], [15, 2], [9, 2], [7, 2], [11, 2, 18, 2], [8 ,2]])
        self.assertEqual(test_match.team_2_moves, [[22, 0], [25, 0], [26, 1], [18, 0], [29, 0]])
        self.assertEqual(test_match.update_gamestate(23, 1), 1)
        self.assertEqual(test_match.update_gamestate(10, 3), 1)
        self.assertEqual(test_match.update_gamestate(18, 0), 1)
        self.assertEqual(test_match.update_gamestate(4, 3), 1)
        self.assertEqual(test_match.update_gamestate(31, 1), 1)
        self.assertEqual(test_match.update_gamestate(3, 2), 1)
        self.assertEqual(test_match.update_gamestate(22, 1), 1)
        self.assertEqual(test_match.update_gamestate(13, 3), 2)
        self.assertEqual(test_match.update_gamestate(22, 3), 1)
        self.assertEqual(test_match.update_gamestate(30, 0), 1)
        self.assertEqual(test_match.update_gamestate(31, 1), 1)
        self.assertEqual(test_match.update_gamestate(20, 0), 1)
        self.assertEqual(test_match.update_gamestate(22, 3), 1)
    
    def test_is_game_over(self):
        test_match = checkers.game.CheckersMatch()
        self.assertEqual(test_match.is_game_over(), 2)
        test_match.turns_since_capture = 80
        self.assertEqual(test_match.is_game_over(), 0)
        test_match.current_gamestate.board = [ 0,  1,  1,  0,      # | | | |o| |o| | |
                                               0,  1,  0,  2,      # | | |o| | | |O| |
                                               0,  0,  0,  0,      # | | | | | | | | |
                                               0,  0,  0,  0,      # | | | | | | | | |
                                               0,  0,  0,  0,      # | | | | | | | | |
                                               0,  0,  1,  0,      # | | | | |o| | | |
                                               0,  0,  0,  0,      # | | | | | | | | |
                                               0,  0,  0,  2]      # | | | | | | |O| |
        test_match.turns_since_capture = 0
        test_match.current_gamestate.turn = -1
        self.assertEqual(test_match.is_game_over(), 1)
        test_match.current_gamestate.board = [ 0,  0,  0,  0,      # | | | | | | | | |
                                               0,  0,  0,  0,      # | | | | | | | | |
                                               0,  0,  0,  0,      # | | | | | | | | |
                                               0,  0,  0,  0,      # | | | | | | | | |
                                               0,  0,  0,  0,      # | | | | | | | | |
                                               0,  1,  0,  0,      # | | |o| | | | | |
                                              -1, -1,  0,  0,      # | |x| |x| | | | |
                                              -1,  0, -1,  0]      # |x| | | |x| | | |
        test_match.current_gamestate.turn = 1
        self.assertEqual(test_match.is_game_over(), -1)
        

if __name__ == "__main__":
    #unittest.main()
    test_match = checkers.game.CheckersMatch()
    test_match.start()