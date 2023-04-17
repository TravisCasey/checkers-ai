"""The command line interface build for playing checkers.

This module can be run as a script to start a command line interface to
play checkers. The command_line_interface function can be called with
a customized tuple of player classes and a match class to run an
interface on those parameters.

Functions:
    command_line_interface: Runs an interface to play checkers in the
        terminal.
"""


def command_line_interface(player_classes, match_class):
    """Begins a checkers match played or observed through the terminal.
     
    Args:
        player_classes: A tuple of classes; these are expected as
            subclasses of the Player class from the players module.
            These are the choices of player types in the match.
        match_class: The CheckersMatch class of which to instantiate.
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

        if class_1_input not in range(len(player_classes)):
            print('Please enter an integer from the list above.')
            continue

        verbose_1_input = input('Show board? (Y/N): ')
        if verbose_1_input in ('y', 'Y'):
            verbose_1 = True
            break
        elif verbose_1_input in ('n', 'N'):
            verbose_1 = False
            break
        else:
            print('Please enter Y for yes or N for no.')

    # Choose second player
    while True:
        for ind in range(len(player_classes)):
            print('{} - {}'.format(ind, player_classes[ind].name))

        try:
            class_2_input = int(input('Choose the second player: '))
        except ValueError:
            print('Please enter an integer from the list above.')
            continue

        if class_2_input not in range(len(player_classes)):
            print('Please enter an integer from the list above.')
            continue
        
        verbose_2_input = input('Show board? (Y/N): ')
        if verbose_2_input in ('y', 'Y'):
            verbose_2 = True
            break
        elif verbose_2_input in ('n', 'N'):
            verbose_2 = False
            break
        else:
            print('Please enter Y for yes or N for no.')

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

    player_1 = player_classes[class_1_input](verbose_1)
    player_2 = player_classes[class_2_input](verbose_2)
    checkers_match = match_class(player_1,
                                 player_2,
                                 game_count_input,
                                 best_of)

    match_result = checkers_match.match_loop()
    print('Team 1: {}\nTeam 2: {}'.format(player_1.name, player_2.name))
    print('Team 1 score: {}\nTeam 2 score: {}\nTeam 1 wins: {}\n\
Team 2 wins: {}\nDraws: {}'.format(*match_result))


if __name__ == '__main__':
    import game
    import players

    command_line_interface((players.Player,
                            players.RandomPlayer,
                            players.EasyPlayer,
                            players.MediumPlayer,
                            players.HardPlayer),
                           game.CheckersMatch)
