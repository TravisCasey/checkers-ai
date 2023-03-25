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

    def test_board_visualization_beginning(self):
        self.assertEqual(checkers.game.vizualize_board([ 1,  1,  1,  1,
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
        self.assertEqual(checkers.game.vizualize_board([-2,  0,  1,  1,
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
        self.assertEqual(checkers.game.vizualize_board([0, 2, 1, 4, 5]), "error")
        

if __name__ == "__main__":
    unittest.main()