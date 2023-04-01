""" This file contains the Player class, and various subclasses. These subclasses make up the various ways moves are chosen. 
"""

class Player():
    """ The Player"""

    def __init__(self):
        self.name = 'manual'

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
