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
LOSS = 0.0
DRAW = 0.5
INVALID_MOVE = -1.0

"""
Playing:
- play game of go through the host
- against all players
- select best moves based on q value tables
"""
"""
Game Tree: It is a structure in the form of a tree consisting of all the possible moves which allow you to move 
from a state of the game to the next state. 
Initial state: It comprises the position of the board and showing whose move it is. 
Successor function: It defines what the legal moves a player can make are. Terminal state: It is the position of the 
board when the game gets over. 
Utility function: It is a function which assigns a numeric value for the outcome of a game. A utility function can 
also be called a payoff function. The utility can be calculated by the current score. 

"""


class TreeNode:
    def __init__(self, game):
        self.parent = None
        self.state = game.state_string()
        self.node_type = None  # min or max
        self.children = [{}]
        self.value = None

    def add_child(self, game, agent):
        new_node = TreeNode(game)
        new_node.parent = self
        new_node.value = new_node.set_child_value(game, agent)
        return new_node

    def set_child_value(self, game, agent):
        if self.node_type == "min":  # get adversaries score for min node
            self.value = game.score(1 if agent.identity is 2 else 2)
        elif self.node_type == "max":
            self.value = game.score(agent.identity)

    def is_root(self):
        if self.parent is None:
            return True
        return False

    def is_leaf(self):
        if not self.children:
            return True
        return False

    def get_tree_root(self):
        current = self
        while current.parent is not None:
            current = current.parent
        return current


class Minimax_agent:

    def __init__(self, go, max_depth=4, piece_type=None, agent_type="Minimax"):
        self.max_depth = max_depth
        self.identity = piece_type  # piece_type = 1 if X and 2 if O
        self.node_expanded = 0
        self.curr_score = 0
        self.agent_type = agent_type
        self.game_tree_root = self.create_game_tree(go)

    def create_game_tree(self, go):
        node = TreeNode()
        actions = self.possible_actions(go.state_string("Current"))
        for action in actions:
            node.add_child(go, self)
        return node

    def evaluation_function(self, go, piece_type):
        score = go.score(piece_type)
        if piece_type == self.identity:
            self.curr_score = score
        return score

    def possible_actions(self, state):
        pass

    def current_state(self, go):
        self.curr_board = go.board

    def result_function(self):
        return 0

    def get_input(self, go):
        pass

    def min_alpha_beta(self, alpha, beta):

        minv = 2

        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(GO_SIZE):
            for j in range(GO_SIZE):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max_alpha_beta(alpha, beta)
                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'

                    if minv <= alpha:
                        return (minv, qx, qy)

                    if minv < beta:
                        beta = minv

        return (minv, qx, qy)

    def max_alpha_beta(self, alpha, beta):
        maxv = -2
        px = None
        py = None

        result = self.is_end()

        if result == 'X':
            return (-1, 0, 0)
        elif result == 'O':
            return (1, 0, 0)
        elif result == '.':
            return (0, 0, 0)

        for i in range(GO_SIZE):
            for j in range(GO_SIZE):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, in_j) = self.min_alpha_beta(alpha, beta)
                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'

                    if maxv >= beta:
                        return (maxv, px, py)

                    if maxv > alpha:
                        alpha = maxv

        return (maxv, px, py)


if __name__ == "__main__":
    N = 5
    game_piece_type, previous_board, board = readInput(N)
    go_game = Game(N)
    go_game.set_board(game_piece_type, previous_board, board)
    player = Minimax_agent(go_game)
    next_action = player.get_input(go_game)
    writeOutput(next_action)
    # st = time.time()
    # go = GO(N)
    # go.set_board(piece_type, previous_board, board)
    # player = Q_learning_agent()
    # player.load_dict(100000)
    # print(player.q_values)
    # # player.epsilon_greedy(player.q_values[str(go.board)], go, 1)
    # print(time.time() - st)
