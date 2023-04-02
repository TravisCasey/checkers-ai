import players


def command_line_interface(player_class_tuple):
    if type(player_class_tuple) is not tuple:
        raise TypeError('Expected player_class_tuple input as a list')
    if len(player_class_tuple) == 0:
        raise TypeError('Expected player_class_tuple input as a nonempty list')
    for player_class in player_class_tuple:
        if not issubclass(player_class, players.Player):
            raise TypeError('Expected player_class_tuple input to contain subclasses of the Player class')
    
    # Choose first player
    for player_class in player_class_tuple:
        print(player_class.__name__)






if __name__ == '__main__':
    command_line_interface((players.Player, players.RandomPlayer))