import copy
import filecmp
import pickle
import sys
import time
import argparse
from my_player3 import GO_SIZE
from my_player3 import Q_learning_agent
from mygame import Game
from read import readInput, readOutput
from write import writeOutput, writeNextInput
from random_player import RandomPlayer
from Minimax import Minimax
import json

X = 1
O = 2
TEST_GAMES = 1000
GAME_SIZE = GO_SIZE

def stringify_keys(d):
    """Convert a dict's keys to strings if they are not."""
    for key in d.keys():

        # check inner dict
        if isinstance(d[key], dict):
            value = stringify_keys(d[key])
        else:
            value = d[key]

        # convert nonstring to string if needed
        if not isinstance(key, str):
            try:
                d[str(key)] = value
            except Exception:
                try:
                    d[repr(key)] = value
                except Exception:
                    raise

            # delete old key
            del d[key]
    return d

if __name__ == "__main__":
            # if self.identity == 1:
    num_games = 0
    state_q_X = pickle.load(open("qvalues_X_{}.pkl".format(num_games), "rb"))
    state_q_O = pickle.load(open("qvalues_O_{}.pkl".format(num_games), "rb"))

    state_q_O = stringify_keys(state_q_O)
    state_q_X = stringify_keys(state_q_X)

    with open("X_dict.json", "w") as file:
        file.write(json.dumps(state_q_X, sort_keys=True, indent=4))
    with open("O_dict.json", "w") as file:
        file.write(json.dumps(state_q_O, sort_keys=True, indent=4))


    