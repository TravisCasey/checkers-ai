import random
""" This file contains the Player class, and various subclasses. These subclasses make up the various ways moves are chosen. 
"""

class Player():
    """ The Player"""
    name = "Manual Player"
    def __init__(self):
        self.gamestate = None

    def get_next_turn(self, message = ''):
        print(message)
        while True:
            try:
                position = int(input('Position: '))
                break
            except ValueError:
                print('Enter a position integer between 0 and 31.')
        
        while True:
            try:
                move_direction = int(input('Direction: '))
                break
            except ValueError:
                print('Enter a direction integer between 0 and 3.')

        return [position, move_direction]
    

class RandomPlayer(Player):
    name = "Random Player"

    def get_next_turn(self, message = ''):
        move_list = self.gamestate.get_valid_moves()
        return move_list[random.randrange(len(move_list))]


