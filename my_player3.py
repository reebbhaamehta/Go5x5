# 7042208305 :Reebbhaa Mehta
import pickle

from read import readInput
from write import writeOutput
import json
from host import GO
import numpy
import json

GO_SIZE = 5
WIN = 1.0
LOSS = -1.0
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
    """
    Q learning agent class should contain:
    state: current pieces on the board, if it is black or white's turn
    actions: possible next states. 5x5 board with
    q_values:
    constructor:
        alpha
        gamma
        q values: dictionary of state, action tuples as keys and q values as values.
        initial values
        states_to_update: list of states visited that need to be updated after a game.
        agent_type: Playing or Learning
        piece_type: 1 for black, 2 for white

    update_Qvalues:

    next_move:

    select_best_action:

    maxQ:
    """

    def __init__(self, piece_type=None, alpha=0.7, gamma=0.9, agent_type="Learning",
                 initial=numpy.random.rand(GO_SIZE, GO_SIZE)):
        self.alpha = alpha
        self.gamma = gamma
        self.initial_values = initial
        self.q_values = {}
        self.states_to_update = []
        self.agent_type = agent_type  # either learning or playing
        self.type = "mine"
        self.identity = piece_type

    def load_dict(self):
        self.q_values = pickle.load(open("dict", "rb"))

    def save_dict(self):
        pickle.dump(self.q_values, open("dict", "wb"))


    def add_state(self, state):
        if state not in self.q_values:
            # action_mat = numpy.zeros((5, 5))
            # action_mat.fill(self.initial_values)
            action_mat = self.initial_values
            self.q_values[state] = action_mat
            tep = self.q_values
            l = len(self.q_values)
        return self.q_values[state]

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
            for i, j in valid_places:
                if qvalues[i][j] > curr_max:
                    curr_max = qvalues[i][j]
                    action = (i, j)

        return action

    # def select_best_action(self, go, piece_type):
    #     state = str(go.board)
    #     q_vals = self.add_state(state)
    #     return self.max_qvalue(q_vals, go, piece_type)

    def get_input(self, go, piece_type):
        if self.identity != piece_type and go.score(piece_type) <= 0:
            self.identity = piece_type
        if go.game_end(piece_type):
            return
        # action = self.select_best_action(go, piece_type)
        state = str(go.board)
        q_vals = self.add_state(state)
        action = self.max_qvalue(q_vals, go, piece_type)
        self.states_to_update.append((go.board, action))
        return action  # returns new state action pair

    def update_Qvalues(self, go):
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

        pickle.dump(self.q_values, open("dict", "wb"))

        self.states_to_update = []


if __name__ == "__main__":
    N = 5
# piece_type, previous_board, board = readInput(N)
# go = GO(N)
# go.set_board(piece_type, previous_board, board)
#
# player = Q_learning_agent(piece_type)
# if go.game_end(1):
#     player.update_Qvalues(go)
# action = player.get_input(go, piece_type)
# writeOutput(action)
