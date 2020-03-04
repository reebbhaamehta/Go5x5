# 7042208305 :Reebbhaa Mehta
import copy
import math
import pickle
import time
import random

from read import readInput
from write import writeOutput
from game import Game
import numpy
import json

GO_SIZE = 5
WIN = 1.0
LOSS = 0
DRAW = 0.5
INVALID_MOVE = -1.0

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
    LEARN_GAMES = 10 ** 6
    REDUCE_E_BY = 0.977
    INCREASE_A_BY = 30

    def __init__(self, piece_type=None, epsilon=0.9, alpha=0.1, gamma=0.9, agent_type="Learning",
                 initial=numpy.random.rand(GO_SIZE, GO_SIZE), learn=True):
        self.gamma = gamma
        self.q_values = {}
        self.states_to_update = []
        self.agent_type = agent_type  # either learning or playing
        self.type = "mine"
        self.identity = piece_type
        self.learn = learn
        self.epsilon = epsilon
        self.alpha = alpha
        self.min_epsilon = 0.05
        self.policy = {}
        self.max_alpha = 0.95
        self.policy_dump_time = 0
        self.varyA_E = True

    def fight(self):
        self.learn = False
        self.varyA_E = False
        self.epsilon = 0
        self.alpha = 1
        self.policy_dump_time = 1583230107
        self.load_policy()

    def save_policy(self):
        for states in self.q_values:
            max_q = -math.inf
            for action in self.q_values[states]:
                if self.q_values[states][action] > max_q:
                    max_q = self.q_values[states][action]
                    self.policy[states] = action
        self.policy_dump_time = int(time.time())
        # print(self.policy)
        pickle.dump(self.policy, open("policy_learned_{}.pkl".format(self.policy_dump_time), "wb"))

    def load_policy(self):
        self.policy = pickle.load(open("policy_learned_{}.pkl".format(self.policy_dump_time), "rb"))

    def load_dict(self, num_games):
        self.q_values = pickle.load(open("qvalues_{}.pkl".format(num_games), "rb"))

    def save_dict(self, num_games):
        pickle.dump(self.q_values, open("qvalues_{}.pkl".format(num_games), "wb"))

    def add_state(self, state):
        if state not in self.q_values:
            action_q = {}
            for i in range(GO_SIZE):
                for j in range(GO_SIZE):
                    poss_action = (i, j)
                    action_q[poss_action] = random.random()
            action_q["PASS"] = random.random()
            self.q_values[state] = action_q
        return self.q_values[state]

    def max_qvalue(self, go, piece_type):
        state = go.state_string()
        action_q_vals = self.add_state(state)
        curr_max = -math.inf
        valid_places = []
        for actions in action_q_vals:
            if actions != "PASS":
                if go.valid_place_check(actions[0], actions[1], piece_type, test_check=True):
                    valid_places.append(actions)
                else:
                    action_q_vals[actions] = INVALID_MOVE
        if not valid_places:
            action = "PASS"
        else:
            if random.random() < self.epsilon:
                action = random.choice(valid_places)
            else:
                for i, j in valid_places:
                    if action_q_vals[(i, j)] > curr_max:
                        curr_max = action_q_vals[(i, j)]
                        action = (i, j)
        return action

    def get_input(self, go, piece_type):
        # if self.identity != piece_type and go.score(piece_type) <= 0:
        #     self.identity = piece_type
        if go.game_end(piece_type):
            return
        action = self.max_qvalue(go, piece_type)
        self.states_to_update.append((go.state_string(), action))
        return action  # returns new state action pair or PASS

    def get_input_policy(self, go, piece_type):
        # if self.identity != piece_type and go.score(piece_type) <= 0:
        #     self.identity = piece_type
        if go.game_end(piece_type):
            return
        state = go.state_string()
        if state in self.policy:
            action = self.policy[state]
        else:
            while True:
                action = random.choice(list(self.policy.values()))
                if action != "PASS":
                    if go.valid_place_check(action[0], action[1], piece_type, test_check=True):
                        return action
        # action = self.max_qvalue(go, piece_type)
        self.states_to_update.append((go.state_string(), action))
        return action  # returns new state action pair or PASS

    def update_epsilon(self):
        if self.varyA_E:
            self.epsilon = max(self.epsilon * self.REDUCE_E_BY, self.min_epsilon)

    def update_alpha(self):
        # self.alpha = min(self.max_alpha, self.alpha * self.INCREASE_A_BY)
        if self.varyA_E:
            self.alpha = 1 - self.epsilon

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
        first_iteration = True
        self.states_to_update.reverse()
        for state, move in self.states_to_update:
            self.q_values[state] = self.add_state(state)
            # TODO: what if you are propagating a loss?? Will you enter this also when not the reward?
            # Try using first_iteration instead as condition to enter this first if.
            # if first_iteration:
            if max_q_value < 0:
                self.q_values[state][move] = reward
                first_iteration = False
            else:
                self.q_values[state][move] = self.q_values[state][move] * (1 - self.alpha) \
                                             + self.alpha * self.gamma * max_q_value
            max_q_value = max(self.q_values[state].values())
        if num_game % int(self.LEARN_GAMES / 100) == 0:
            self.update_epsilon()
            self.update_alpha()
        if num_game % int(self.LEARN_GAMES / 100) == 0:
            self.save_dict(num_game)
            self.save_policy()
        self.states_to_update = []


if __name__ == "__main__":
    N = 5
    game_piece_type, previous_board, board = readInput(N)
    go_game = Game(N)
    go_game.set_board(game_piece_type, previous_board, board)
    player = Q_learning_agent()
    Q_learning_agent.identity = game_piece_type
    player.fight()
    next_action = player.get_input(go_game, game_piece_type)
    writeOutput(next_action)
