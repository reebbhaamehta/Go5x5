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
Game Tree: It is a structure in the form of a tree consisting of all the possible moves which allow you to move 
from a state of the game to the next state. 
Initial state: It comprises the position of the board and showing whose move it is. 
Successor function: It defines what the legal moves a player can make are. Terminal state: It is the position of the 
board when the game gets over. 
Utility function: It is a function which assigns a numeric value for the outcome of a game. A utility function can 
also be called a payoff function. The utility can be calculated by the current score. 

"""



class Minimax:
    LEARN_GAMES = 10 ** 6
    REDUCE_E_BY = 0.977
    INCREASE_A_BY = 0.03

    # TODO: make alpha increase over time so that it makes more sense keep a max or min alpha so that
    def __init__(self, piece_type=None, agent_type="Minimax"):

    def current_state(self):



if __name__ == "__main__":
    N = 5
    game_piece_type, previous_board, board = readInput(N)
    go_game = Game(N)
    go_game.set_board(game_piece_type, previous_board, board)
    player = Q_learning_agent()
    player.load_dict(100000)
    next_action = player.get_input(go_game, game_piece_type)
    writeOutput(next_action)
    # st = time.time()
    # go = GO(N)
    # go.set_board(piece_type, previous_board, board)
    # player = Q_learning_agent()
    # player.load_dict(100000)
    # print(player.q_values)
    # # player.epsilon_greedy(player.q_values[str(go.board)], go, 1)
    # print(time.time() - st)
