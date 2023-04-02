import game
import players


def command_line_interface(player_class_tuple, match_class):
    if type(player_class_tuple) is not tuple:
        raise TypeError('Expected player_class_tuple input as a list')
    if len(player_class_tuple) == 0:
        raise TypeError('Expected player_class_tuple input as a nonempty list')
    for player_class in player_class_tuple:
        if not issubclass(player_class, players.Player):
            raise TypeError('Expected player_class_tuple input to contain subclasses of the Player class')

    # Choose first player
    while True:
        for class_index in range(len(player_class_tuple)):
            print('{} - {}'.format(class_index, player_class_tuple[class_index].name))
        try:
            class_1_input = int(input('Choose the first player: '))
        except:
            print('Please enter an integer from the list above.')
            continue
        if class_1_input in range(len(player_class_tuple)):
            break
        else:
            print('Please enter an integer from the list above.')
    
    # Choose second player
    while True:
        for class_index in range(len(player_class_tuple)):
            print('{} - {}'.format(class_index, player_class_tuple[class_index].name))
        try:
            class_2_input = int(input('Choose the second player: '))
        except:
            print('Please enter an integer from the list above.')
            continue
        if class_2_input in range(len(player_class_tuple)):
            break
        else:
            print('Please enter an integer from the list above.')
    
    # Choose number of games to play
    while True:
        try:
            game_count_input = int(input('Choose number of games to play: '))
        except:
            print('Please enter a positive integer.')
            continue
        if game_count_input > 0:
            break
        else:
            print('Please enter a positive integer.')
    
    # Start match
    team_1_player = player_class_tuple[class_1_input]()
    team_2_player = player_class_tuple[class_2_input]()
    current_game_count = 0
    checkers_match = match_class(team_1_player, team_2_player)
    win_1_count = 0
    win_2_count = 0
    draw_count = 0
    
    while current_game_count < game_count_input:
        if current_game_count % 10 == 0:
            print('({}/{})'.format(current_game_count, game_count_input))
        checkers_match.__init__(team_1_player, team_2_player)
        result = checkers_match.start()
        match result:
            case 1:
                win_1_count += 1
            case 0:
                draw_count += 1
            case -1:
                win_2_count += 1
        current_game_count += 1
    
    print('Team 1 wins: {}\nTeam 2 wins: {}\nDraws: {}'.format(win_1_count, win_2_count, draw_count))


if __name__ == '__main__':
    command_line_interface((players.Player, players.RandomPlayer), game.CheckersMatch)