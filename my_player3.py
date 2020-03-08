# 7042208305 :Reebbhaa Mehta
import copy
import math
import pickle
import time
import random

from read import readInput
from write import writeOutput
from mygame import Game
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


def string_to_state(state_string):
    state = numpy.fromstring(state_string, dtype=int, sep=" ")
    state = numpy.reshape(state, (5, 5))
    return state


def state_to_string(state):
    state_string = str(state.ravel())[1:-1].strip()
    return state_string


def orient_action(action, orientation):
    # rotate left
    for i in range(orientation[0]):
        action = (GO_SIZE - 1 - action[1], action[0])
    # flip with x axis static
    if orientation[1] == 0:
        action = (GO_SIZE - 1 - action[0], action[1])
    return action


def orient_action_to_base(action, orientation):
    # rotate right
    for i in range(orientation[0]):
        action = (action[1], GO_SIZE - 1 - action[0])
    # flip with x axis static
    if orientation[1] == 0:
        action = (GO_SIZE - 1 - action[0], action[1])
    return action


def symmetrical_states(current_board):
    # print(type(current_board))
    # exit()
    # state_list = [(equivalent_board, (rotation(counterclockwise) = 0, 1, 2, 3,
    #               axis to flip = -1 -> no flips, 0->x axis static, 1->y axis static))]
    state_list = [(current_board, (0, -1))]  # original board
    for i in range(0, 3):
        state_list.append((numpy.rot90(state_list[i][0]), (i+1, -1)))
    for i in range(4):
        rotations = state_list[i][1][0]
        orientation = (rotations, 1)
        state_list.append((numpy.flip(state_list[i][0], 0), orientation))
    # state = game.state_string()
    return state_list


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
        self.policy_X = {}
        self.policy_O = {}
        self.max_alpha = 0.95
        self.varyA_E = True
        self.state_q_O = {}
        self.state_q_X = {}
        self.file_count = 0

    def fight(self):
        self.learn = False
        self.varyA_E = False
        self.epsilon = 0
        self.alpha = 1
        self.policy_dump_time = 1583230107
        self.load_policy()

    def save_policy(self, num_games):
        for states in self.state_q_X:
            max_q = -math.inf
            for action in self.state_q_X[states]:
                if self.state_q_X[states][action] > max_q:
                    max_q = self.state_q_X[states][action]
                    self.policy_X[states] = action
        for states in self.state_q_O:
            max_q = -math.inf
            for action in self.state_q_O[states]:
                if self.state_q_O[states][action] > max_q:
                    max_q = self.state_q_O[states][action]
                    self.policy_O[states] = action
        pickle.dump(self.policy_X, open("policy_learned_X_{}.pkl".format(num_games), "wb"))
        pickle.dump(self.policy_O, open("policy_learned_O_{}.pkl".format(num_games), "wb"))

    def load_policy(self, num_games):
        self.policy_X = pickle.load(open("policy_learned_X_{}.pkl".format(num_games), "rb"))
        self.policy_O = pickle.load(open("policy_learned_O_{}.pkl".format(num_games), "rb"))

    def load_dict(self, num_games):
        # if self.identity == 1:
        self.state_q_X = pickle.load(open("qvalues_X_{}.pkl".format(num_games), "rb"))
        # else:
        self.state_q_O = pickle.load(open("qvalues_O_{}.pkl".format(num_games), "rb"))

    def save_dict(self, num_games):
        # if self.identity == 1:
        pickle.dump(self.state_q_X, open("qvalues_X_{}.pkl".format(num_games), "wb"))
        # else:
        pickle.dump(self.state_q_O, open("qvalues_O_{}.pkl".format(num_games), "wb"))

    def state_q_values_O(self, state):
        state_np = string_to_state(state)
        symmetries = symmetrical_states(state_np)
        initial_state = state_to_string(symmetries[0][0])
        symm_index = [state_to_string(s[0]) in self.state_q_O for s in symmetries]
        if not any(symm_index):
            # actions_q_values = {}
            self.state_q_O[initial_state] = {}
            for i in range(GO_SIZE):
                for j in range(GO_SIZE):
                    possible_action = (i, j)
                    self.state_q_O[initial_state][possible_action] = random.random()
            self.state_q_O[initial_state]["PASS"] = random.random()
            # self.state_q[initial_state] = actions_q_values
            orientation = (0, -1)
            return self.state_q_O[initial_state], orientation, initial_state
        else:
            orientation = symmetries[symm_index.index(True)][1]
            base_state = state_to_string(symmetries[symm_index.index(True)][0])
            return self.state_q_O[base_state], orientation, base_state

    def state_q_values_X(self, state):
        state_np = string_to_state(state)
        symmetries = symmetrical_states(state_np)
        initial_state = state_to_string(symmetries[0][0])
        symm_index = [state_to_string(s[0]) in self.state_q_X for s in symmetries]
        if not any(symm_index):
            # actions_q_values = {}
            self.state_q_X[initial_state] = {}
            for i in range(GO_SIZE):
                for j in range(GO_SIZE):
                    possible_action = (i, j)
                    self.state_q_X[initial_state][possible_action] = random.random()
            self.state_q_X[initial_state]["PASS"] = random.random()
            # self.state_q[initial_state] = actions_q_values
            orientation = (0, -1)
            return self.state_q_X[initial_state], orientation, initial_state
        else:
            orientation = symmetries[symm_index.index(True)][1]
            base_state = state_to_string(symmetries[symm_index.index(True)][0])
            return self.state_q_X[base_state], orientation, base_state

    def max_qvalue(self, go, piece_type):
        # state_base_orientation, orientation = symmetrical_states(go.board)
        # print(states_orientation)
        state = state_to_string(go.board)
        if self.identity == 1:
            action_q_vals, orientation, base_state = self.state_q_values_X(state)
        else:
            action_q_vals, orientation, base_state = self.state_q_values_O(state)
        curr_max = -math.inf
        valid_places = []
        for actions in action_q_vals:
            if actions != "PASS":
                actual_orientation_action = orient_action(actions, orientation)
                if go.valid_place_check(actual_orientation_action[0], actual_orientation_action[1], piece_type, test_check=True):
                    action_in_base = orient_action_to_base(actual_orientation_action, orientation)
                    valid_places.append(action_in_base)
                # else:
                #     action_q_vals[actions] = INVALID_MOVE
        # print(valid_places)
        if not valid_places:
            action = "PASS"
            action_base = "PASS"
        else:
            if random.random() < self.epsilon:
                action_base = random.choice(valid_places)
            else:
                for i, j in valid_places:
                    if action_q_vals[(i, j)] > curr_max:
                        curr_max = action_q_vals[(i, j)]
                        action_base = (i, j)
            action = orient_action(action_base, orientation)
        self.states_to_update.append((base_state, action_base))
        return action

    def get_input(self, go, piece_type):
        if self.identity != piece_type and go.score(piece_type) <= 0:
            self.identity = piece_type
        if go.game_end():
            return
        action = self.max_qvalue(go, piece_type)
        # self.states_to_update.append((go.state_string(), action))
        return action  # returns new state action pair or PASS

    def get_input_policy(self, go, piece_type):
        # if self.identity != piece_type and go.score(piece_type) <= 0:
        #     self.identity = piece_type
        if go.game_end():
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
            if self.identity == 1:
                base_state_action_q, orientation, base_state = self.state_q_values_X(state)
            else:
                base_state_action_q, orientation, base_state = self.state_q_values_O(state)
            # TODO: what if you are propagating a loss?? Will you enter this also when not the reward?
            # Try using first_iteration instead as condition to enter this first if.
            # if max_q_value < 0:
            #     self.q_values[state][move] = reward
            if first_iteration:
                base_state_action_q[move] = reward
                first_iteration = False
            else:
                # self.q_values[state][move] = self.q_values[state][move] * (1 - self.alpha) \
                                             # + self.alpha * self.gamma * max_q_value
                base_state_action_q[move] = base_state_action_q[move] * (1 - self.alpha) \
                                            + self.alpha * self.gamma * max_q_value
            max_q_value = max(base_state_action_q.values())
        if num_game % int(self.LEARN_GAMES / 100) == 0:
            self.update_epsilon()
            self.update_alpha()
        if num_game % int(self.LEARN_GAMES / 100) == 0:
            if self.file_count == 5:
                self.file_count = 0
            self.save_dict(self.file_count)
            self.save_policy(self.file_count)
            self.file_count += 1
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
