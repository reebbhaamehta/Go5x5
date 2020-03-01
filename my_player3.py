# 7042208305 :Reebbhaa Mehta
import copy
import pickle
import time
import random

from read import readInput
from write import writeOutput
import json
from host import GO
import numpy
import json

GO_SIZE = 5
WIN = 1.0
LOSS = -1.0
DRAW = 0.5  # TODO: change this to 0 maybe?
INVALID_MOVE = -1.0
REDUCE_E_BY = 0.977

"""
Playing:
- play game of go through the host
- against all players
- select best moves based on q value tables
"""
"""
Learning:
- play game of go through the host
- against random player & then itself
- select best moves based on q value tables
- update Q values after each game
- update table of q values for each state
"""


class Q_learning_agent:

    LEARN_GAMES = 10 ** 4
    REDUCE_E_BY = 0.977

    # TODO: make alpha increase over time so that it makes more sense keep a max or min alpha so that
    def __init__(self, piece_type=None, alpha=0.7, gamma=0.9, agent_type="Learning",
                 initial=numpy.random.rand(GO_SIZE, GO_SIZE), learn=True, epsilon=1):
        self.alpha = alpha
        self.gamma = gamma
        self.initial_values = initial  # numpy.random.rand(GO_SIZE, GO_SIZE)
        self.q_values = {}
        self.states_to_update = []
        self.agent_type = agent_type  # either learning or playing
        self.type = "mine"
        self.identity = piece_type
        self.learn = learn
        self.epsilon = epsilon
        self.min_epsilon = 0.01

    def load_dict(self, num_games):
        self.q_values = pickle.load(open("qvalues_{}.pkl".format(num_games), "rb"))

    def save_dict(self, num_games):
        pickle.dump(self.q_values, open("qvalues_{}.pkl".format(num_games), "wb"))

    def add_state(self, state):
        if state not in self.q_values:
            # action_mat = numpy.zeros((5, 5))
            # action_mat.fill(self.initial_values)
            action_mat = self.initial_values
            self.q_values[state] = action_mat
        return self.q_values[state]

    # TODO:EPSILON GREEDY POLICY LEARNING: TART WITH EPSILON REALLY LARGE LIKE 90%
    #  SO YOU EXLPORE 90% OF THE TIME AND DECREASE IT OVER TIME THAT YOU EXPLORE MORE STATES.
    def max_qvalue(self, qvalues, go, piece_type):
        curr_max = -numpy.inf
        valid_places = []
        for i in range(GO_SIZE):
            for j in range(GO_SIZE):
                if go.valid_place_check(i, j, piece_type, test_check=True):
                    valid_places.append((i, j))
        if not valid_places:
            action = "PASS"
        else:
            if random.random() < self.epsilon:
                action = random.choice(valid_places)
            else:

                for i, j in valid_places:
                    if qvalues[i][j] > curr_max:
                        curr_max = qvalues[i][j]
                        action = (i, j)
        return action

    def update_epsilon(self):
        self.epsilon = max(self.epsilon * self.REDUCE_E_BY, self.min_epsilon)

    def get_input(self, go, piece_type):
        if self.identity != piece_type and go.score(piece_type) <= 0:
            self.identity = piece_type
        if go.game_end(piece_type):
            return
        # action = self.select_best_action(go, piece_type)
        state = str(go.board)
        q_vals = self.add_state(state)
        action = self.max_qvalue(q_vals, go, piece_type)
        self.states_to_update.append((go.state_string(), action))
        # print(self.states_to_update[len(self.states_to_update)-1])
        return action  # returns new state action pair

    def update_Qvalues(self, go, num_game):
        # after a game update the q table
        # check result to set the reward
        winner = go.judge_winner()
        if winner == self.identity:
            reward = WIN
        elif winner == 0:
            reward = DRAW
        else:
            reward = LOSS
        max_q_value = -1.0
        self.states_to_update = self.states_to_update[::-1]
        for state, move in self.states_to_update:
            if move != "PASS":
                curr_stateQ = self.add_state(str(state))

                if max_q_value < 0:
                    curr_stateQ[move[0]][move[1]] = reward
                else:
                    curr_stateQ[move[0]][move[1]] = curr_stateQ[move[0]][move[1]] * (1 - self.alpha) \
                                                    + self.alpha * self.gamma * max_q_value
                max_q_value = numpy.max(curr_stateQ)

        if num_game % self.LEARN_GAMES / 100 == 0:
            self.update_epsilon()
            print(self.epsilon)
        if num_game % int(self.LEARN_GAMES / 10) == 0:
            self.save_dict(num_game)
        # pickle.dump(self.q_values, open("dict", "wb"))
        # self.save_dict(num_games)
        self.states_to_update = []


if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = Q_learning_agent()
    player.load_dict(100000)
    action = player.get_input(go, piece_type)
    writeOutput(action)
    # st = time.time()
    # go = GO(N)
    # go.set_board(piece_type, previous_board, board)
    # player = Q_learning_agent()
    # player.load_dict(100000)
    # print(player.q_values)
    # # player.epsilon_greedy(player.q_values[str(go.board)], go, 1)
    # print(time.time() - st)
