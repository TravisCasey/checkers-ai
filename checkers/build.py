import game
import players


def command_line_interface(player_classes, match_class):
    """ This function begins a checkers match played or observed through
    the command line. The player_classes input is a tuple of classes;
    these are expected as subclasses of the Player class from the
    players module. The match_class is the CheckersMatch class of which
    to instantiate.
    """

    # Choose first player
    while True:
        for ind in range(len(player_classes)):
            print('{} - {}'.format(ind, player_classes[ind].name))

        try:
            class_1_input = int(input('Choose the first player: '))
        except ValueError:
            print('Please enter an integer from the list above.')
            continue

        if class_1_input in range(len(player_classes)):
            break
        else:
            print('Please enter an integer from the list above.')

    # Choose second player
    while True:
        for ind in range(len(player_classes)):
            print('{} - {}'.format(ind, player_classes[ind].name))

        try:
            class_2_input = int(input('Choose the second player: '))
        except ValueError:
            print('Please enter an integer from the list above.')
            continue

        if class_2_input in range(len(player_classes)):
            break
        else:
            print('Please enter an integer from the list above.')

    # Choose number of games to play
    while True:
        try:
            game_count_input = int(input('Choose number of games to play: '))
        except ValueError:
            print('Please enter a positive integer.')
            continue
        if game_count_input > 0:
            break
        else:
            print('Please enter a positive integer.')

    # Determine if match is best of or not.
    while True:
        best_of_input = input('Best of? (Y/N): ')
        if best_of_input in ('y', 'Y'):
            best_of = True
            break
        elif best_of_input in ('n', 'N'):
            best_of = False
            break
        else:
            print('Please enter Y for yes or N for no.')

    player_1 = player_classes[class_1_input](1)
    player_2 = player_classes[class_2_input](-1)
    checkers_match = match_class(player_1,
                                 player_2,
                                 game_count_input,
                                 best_of)
    match_result = checkers_match.match_loop()
    print('Team 1: {}\nTeam 2: {}'.format(player_1.name, player_2.name))
    print('Team 1 score: {}\nTeam 2 score: {}\nTeam 1 wins: {}\n\
Team 2 wins: {}\nDraws: {}'.format(*match_result))


if __name__ == '__main__':
    command_line_interface((players.Player,
                            players.RandomPlayer,
                            players.EasyPlayer,
                            players.MediumPlayer,
                            players.HardPlayer),
                           game.CheckersMatch)
