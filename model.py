import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count

import torch
from torch import nn
from torch import optim
import torch.nn.functional as F

import checkers


PATH = 'model_params.pt'
BATCH_SIZE = 128
GAMMA = 0.95
EXP_START = 0.9
EXP_END = 0.05
EXP_DECAY = 25000
GENERATIONS = 500
GAMES_PER_GENERATION = 200
LR = 0.0005
WIN_REWARD = 1
WIN_STEP = (1 - GAMMA) * WIN_REWARD
DRAW_REWARD = 0
DRAW_STEP = (1 - GAMMA) * DRAW_REWARD
LOSS_REWARD = -1
LOSS_STEP = (1 - GAMMA) * LOSS_REWARD

plt.ion()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using {}.'.format(device))

# The named tuple Tranisiton stores all information needed to trade the
# on past states.
Transition = namedtuple('Transition',
                        ('state', 'action', 'reward', 'next_state', 'mask'))


class ReplayMemory():
    """ The ReplayMemory class defines an object that stores transition
    data then outputs them to be trained on in random batches. This
    reduces correlation between transitions to better train the model.
    """
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    """ The neural network used for our reinforcement learning."""
    def __init__(self):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(32, 48)
        self.layer2 = nn.Linear(48, 64)
        self.layer3 = nn.Linear(64, 96)
        self.layer4 = nn.Linear(96, 128)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        x = F.relu(self.layer3(x))
        # Results in [-1, 1]
        return (F.tanh(self.layer4(x)))


class TrainPlayer(checkers.players.Player):
    """ This subclass uses the provided neural network to decide on the
    next move to be played. It has a chance to choose a random move for
    exploration with an exponentially decaying distribution. It stores
    gamestates and masks used in memory until the end of the game when the
    reward can be assigned.
    """
    name = 'Training Player'

    def __init__(self):
        self.gamestate = None
        self.iters = 0
        self.temp_memory = [[], []]  # FIXME Tensor?

        # Attempt to initialize model parameters from PATH
        self.model = DQN().to(device)
        try:
            self.model.load_state_dict(torch.load(PATH))
            print('Model loaded successfully.')
        except FileNotFoundError:
            print('No model found, using default values.')

    def to_tuple(self, index):
        """ This method takes in a 2d tensor containing the index of a
        move and converts it into a tuple containing the move used by
        the checkers package.
        """
        pos = int(index.item() // 4)
        dir = int(index.item() % 4)
        return (pos, dir)

    def to_tensor(self, move):
        """ This method takes in a tuple containing a move and converts
        it into a 2d tensor containing the index of the move.
        """
        return torch.tensor([[move[0]*4 + move[1]]],
                            dtype=torch.int64,
                            device=device)

    def orient_board(self):
        """ The model always takes in a board from team 1 perspective.
        If the model is playing for team 2, it must reverse the board to
        appear as the same state but for team 1.
        """
        # FIXME: use numpy array for board?
        board_tensor = torch.tensor([self.gamestate.board],
                                    dtype=torch.float32,
                                    device=device)
        if self.gamestate.turn == 1:
            return board_tensor
        else:
            board_tensor.mul_(-1)
            return board_tensor.flip(1)

    def get_mask(self):
        """ This method returns a 2d array of values corresponding to
        valid moves. Invalid moves have -2, valid has 0. Can be added to
        neura net output to mask out invalid moves.
        """
        valid_moves = self.gamestate.get_valid_moves()
        valid_ind = []
        for move in valid_moves:
            valid_ind.append(move[0]*4 + move[1])
        mask = tuple(map(lambda s: s not in valid_ind, range(128)))
        return torch.tensor([mask], dtype=torch.int64, device=device) * -2

    def get_next_turn(self, opp_move):
        """ This method returns the next move in tuple format. It
        randomly decides to choose either a move from the neural net
        or to decide randomly with an exponentially decaying
        distribution. It then saves state information to construct
        replay memory after the game.
        """
        mask = self.get_mask()
        # Compute current threshold of exponential distribution
        exp_current = EXP_END + (EXP_START - EXP_END)\
            * math.exp(-1 * self.iters / EXP_DECAY)
        self.iters += 1

        if random.random() > exp_current:
            with torch.no_grad():
                move_weights = self.model(self.orient_board())
                move_ind = (move_weights + mask).max(1, keepdim=True)[1]
                chosen_move = self.to_tuple(move_ind)
        else:
            move_list = self.gamestate.get_valid_moves()
            chosen_move = move_list[random.randrange(len(move_list))]
            move_ind = self.to_tensor(chosen_move)
        if self.gamestate.turn == 1:
            self.temp_memory[0].append((self.orient_board(), mask, move_ind))
        else:
            self.temp_memory[1].append((self.orient_board(), mask, move_ind))
        return chosen_move


model_player = TrainPlayer()
target_model = DQN().to(device)
optimizer = optim.AdamW(model_player.model.parameters(), lr=LR, amsgrad=True)
memory = ReplayMemory(10000)


def optimize_model():
    if len(memory) < BATCH_SIZE:
        return
    transitions = memory.sample(BATCH_SIZE)

    batch = Transition(*zip(*transitions))

    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                            batch.next_state)),
                                  dtype=torch.bool,
                                  device=device)
    next_states = torch.cat([s for s in batch.next_state if s is not None])
    state_batch = torch.cat(batch.state)
    mask_batch = torch.cat([s for s in batch.mask if s is not None])
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)

    q_values = model_player.model(state_batch).gather(1, action_batch)

    v_values = torch.zeros(BATCH_SIZE, device=device)
    with torch.no_grad():
        v_values[non_final_mask] = (target_model(next_states)
                                    + mask_batch).max(1)[0]

    expected_q_values = (v_values * GAMMA) + reward_batch

    criterion = nn.SmoothL1Loss()
    loss = criterion(q_values, expected_q_values.unsqueeze(1))
    print(loss.item())

    optimizer.zero_grad()
    loss.backward()

    torch.nn.utils.clip_grad_value_(model_player.model.parameters(), 100)
    optimizer.step()

    return loss.item()


def plot_loss(loss):
    SMOOTHING = 100
    plt.clf()
    plt.title('Training')
    plt.xlabel('Episodes')
    plt.ylabel('Smoothed Loss')
    # plt.plot(loss)

    smoothed_loss = []
    for i in range(len(loss)):
        if i < SMOOTHING - 1:
            smoothed_loss.append(sum(loss[:i+1]) / (i+1))
        else:
            smoothed_loss.append(sum(loss[i-SMOOTHING+1:i+1]) / SMOOTHING)
    plt.plot(smoothed_loss)
    plt.pause(0.001)


# Training loop
loss = []
for generation in range(GENERATIONS):
    print('Generation: ({}/{})'.format(generation, GENERATIONS))
    # Sync model parameters
    target_model.load_state_dict(model_player.model.state_dict())
    for game in range(GAMES_PER_GENERATION):
        checkers_match = checkers.game.CheckersMatch(model_player,
                                                     model_player,
                                                     1,
                                                     False)
        match_result = checkers_match.match_loop()
        if match_result[2] == 1:
            reward_1 = WIN_STEP
            reward_2 = LOSS_STEP
            last_reward_1 = WIN_REWARD
            last_reward_2 = LOSS_REWARD
        elif match_result[3] == 1:
            reward_1 = LOSS_STEP
            reward_2 = WIN_STEP
            last_reward_1 = LOSS_REWARD
            last_reward_2 = WIN_REWARD
        else:
            reward_1 = DRAW_STEP
            reward_2 = DRAW_STEP
            last_reward_1 = DRAW_REWARD
            last_reward_2 = DRAW_REWARD
        reward_1 = torch.tensor([reward_1],
                                dtype=torch.int64,
                                device=device)
        last_reward_1 = torch.tensor([last_reward_1],
                                     dtype=torch.int64,
                                     device=device)
        reward_2 = torch.tensor([reward_2],
                                dtype=torch.int64,
                                device=device)
        last_reward_2 = torch.tensor([last_reward_2],
                                     dtype=torch.int64,
                                     device=device)

        for ind in range(len(model_player.temp_memory[0]) - 1):
            memory.push(model_player.temp_memory[0][ind][0],
                        model_player.temp_memory[0][ind][2],
                        reward_1,
                        model_player.temp_memory[0][ind + 1][0],
                        model_player.temp_memory[0][ind + 1][1])
        memory.push(model_player.temp_memory[0][-1][0],
                    model_player.temp_memory[0][-1][2],
                    last_reward_1,
                    None,
                    None)
        for ind in range(len(model_player.temp_memory[1]) - 1):
            memory.push(model_player.temp_memory[1][ind][0],
                        model_player.temp_memory[1][ind][2],
                        reward_2,
                        model_player.temp_memory[1][ind + 1][0],
                        model_player.temp_memory[1][ind + 1][1])
        memory.push(model_player.temp_memory[1][-1][0],
                    model_player.temp_memory[1][-1][2],
                    last_reward_2,
                    None,
                    None)
        model_player.temp_memory = [[], []]

        new_loss = optimize_model()
        if new_loss is not None:
            loss.append(new_loss)
    plot_loss(loss)
    # Plot progress, validate
