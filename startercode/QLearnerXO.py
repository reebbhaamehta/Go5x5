# 7042208305 :Reebbhaa Mehta
import copy
import math
import pickle
import time
import random

from read import readInput
from write import writeOutput
# from game import Game
import numpy
import json

GO_SIZE = 3
WIN = 1.0
LOSS = 0
DRAW = 0.5
INVALID_MOVE = -1.0


class QLearnerXO:
    GAME_NUM = 10 ** 5  # ** 6
    REDUCE_E_BY = 0.977
    INCREASE_A_BY = 0.03

    # TODO: make alpha increase over time so that it makes more sense keep a max or min alpha so that
    def __init__(self, piece_type=None, epsilon=0, alpha=0.7, gamma=0.9, agent_type="Learning",
                 initial=numpy.random.rand(GO_SIZE, GO_SIZE), learn=True):
        self.gamma = gamma
        self.q_values = {}
        self.states_to_update = []
        self.agent_type = agent_type  # either learning or playing
        self.type = "mine"
        self.identity = piece_type
        # self.learn = learn
        self.epsilon = epsilon
        self.alpha = alpha
        self.min_epsilon = 0.1
        self.policy = {}
        self.max_alpha = 0.9
        self.policy_dump_time = 0
        self.num_game = 1
        self.varyA_E = False
        self.curr_win_rate = 0  # number of games won / number of games played
        self.prev_win_rate = 0

    def set_win_rates(self, wins):
        self.prev_win_rate = self.curr_win_rate
        if self.num_game != 0:
            self.curr_win_rate = int(wins/self.num_game)
        else:
            self.curr_win_rate = 1

    def set_side(self, side):
        self.identity = side

    def save_policy(self):
        for states in self.q_values:
            max_q = -math.inf
            for action in self.q_values[states]:
                if self.q_values[states][action] > max_q:
                    max_q = self.q_values[states][action]
                    self.policy[states] = action
        # print(self.policy)
        pickle.dump(self.policy, open("policy_learned.pkl", "wb"))

    def load_policy(self):
        self.policy = pickle.load(open("policy_learned.pkl", "rb"))

    def load_dict(self):
        self.q_values = pickle.load(open("qvalues.pkl", "rb"))

    def save_dict(self):
        pickle.dump(self.q_values, open("qvalues.pkl", "wb"))

    def add_state(self, state):
        if state not in self.q_values:
            action_q = {}
            for i in range(GO_SIZE):
                for j in range(GO_SIZE):
                    poss_action = (i, j)
                    action_q[poss_action] = random.random()
            # action_q["PASS"] = random.random()
            self.q_values[state] = action_q
        return self.q_values[state]

    def max_qvalue_go(self, go):
        state = go.encode_state()
        action_q_vals = self.add_state(state)
        curr_max = -math.inf
        valid_places = []
        for actions in action_q_vals:
            if go.is_valid_move(actions[0], actions[1]):
                valid_places.append(actions)
            else:
                action_q_vals[actions] = INVALID_MOVE
        if valid_places:
            if random.random() < self.epsilon:
                action = random.choice(valid_places)
            else:
                for i, j in valid_places:
                    if action_q_vals[(i, j)] > curr_max:
                        curr_max = action_q_vals[(i, j)]
                        action = (i, j)
        return action

    def max_qvalue(self, go):
        state = go.encode_state()
        qvalues = self.add_state(state)
        while True:
            curr_max = -math.inf
            for actions in qvalues:
                if qvalues[actions] > curr_max:
                    curr_max = qvalues[actions]
                    action = actions
            if go.is_valid_move(action[0], action[1]):
                return action
            else:
                qvalues[action] = -1.0

    def update_epsilon(self):
        if self.varyA_E:
            self.epsilon = max(self.epsilon * self.REDUCE_E_BY, self.min_epsilon)

    def update_alpha(self):
        # self.alpha = min(self.max_alpha, self.alpha * self.INCREASE_A_BY)
        if self.varyA_E:
            self.alpha = 1 - self.epsilon

    def move(self, go):
        if go.game_over():
            return
        action = self.max_qvalue_go(go)
        self.states_to_update.append((go.encode_state(), action))
        return go.move(action[0], action[1], self.identity)

    def learn(self, go):
        winner = go.game_result
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
            curr = self.add_state(state)
            self.q_values[state] = self.add_state(state)
            # if first_iteration:
            if max_q_value < 0:
                self.q_values[state][move] = reward
                first_iteration = False
            else:
                self.q_values[state][move] = self.q_values[state][move] * (1 - self.alpha) \
                                             + self.alpha * self.gamma * max_q_value
            max_q_value = max(self.q_values[state].values())
        if self.num_game % int(self.GAME_NUM / 100) == 0:
            self.update_epsilon()
            self.update_alpha()
        if self.num_game % int(self.GAME_NUM / 10) == 0:
            self.save_dict()
            self.save_policy()
        self.states_to_update = []

if __name__ == "__main__":
    qlearner = QLearnerXO()
    qlearner.load_policy()
    print(qlearner.policy)