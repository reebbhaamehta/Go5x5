# 7042208305 :Reebbhaa Mehta
from read import readInput
from write import writeOutput

from host import GO
import numpy

WIN = 1.0
LOSS = -1.0
DRAW = 0.5

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

    update_Qvalues:

    next_move:

    select_best_action:

    maxQ:
    """

    def __init__(self, piece_type, alpha, gamma, agent_type, initial=0):
        self.alpha = alpha
        self.gamma = gamma
        self.initial_values = initial
        self.q_values = {}
        self.states_to_update = []
        self.piece = piece_type
        self.agent_type = agent_type  # either learning or playing

    def add_state(self, state):
        if state not in self.q_values:
            action_mat = numpy.zeros((5, 5))
            action_mat.fill(self.initial_values)
            self.q_values[state] = action_mat
        return

    def select_best_action(self, board, state):

        return

    def next_move(self, board):

        return

    def update_Qvalues(self, result):
        # after a game update the q table
        # check result to set the reward
        self.states_to_update = self.states_to_update[::-1]
        for i in self.states_to_update:
            curr_stateQ = self.q_values[i]


class GoBoard:
    """
    class of go board should contain:
    constructor:
        create the board of a fixed size
    is_move_valid: decide if action is valid


    """
    # def __init__(self):
    # self.state = numpy.zeros((5, 5))
