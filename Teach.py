import filecmp
import pickle
import sys

from my_player3 import Q_learning_agent
from host import GO, judge
from read import readInput, readOutput
from write import writeOutput, writeNextInput
from random_player import RandomPlayer

X = 1
O = 2
LEARN_GAMES = 100

"""
Learning:
- play game of go through the host
- against random player & then itself
- select best moves based on q value tables
- update Q values after each game
- update table of q values for each state
"""

if __name__ == "__main__":

    qlearner = Q_learning_agent()

    random_player = RandomPlayer()

    num_games = 0
    for i in range(LEARN_GAMES):
        go = GO(5)
        go.init_board(5)
        go.play(random_player, qlearner, False)
        num_games += 1
        if num_games == 100:
            qlearner.update_Qvalues(go, i + 1)
            num_games = 0

    qlearnerpoint2 = Q_learning_agent()
    qlearnerpoint2.load_dict(LEARN_GAMES)
    num_games = 0

    for i in range(LEARN_GAMES):
        go = GO(5)
        go.init_board(5)
        go.play(qlearnerpoint2, qlearner, False)
        num_games += 1
        if num_games == 100:
            qlearnerpoint2.update_Qvalues(go, i + 1 + LEARN_GAMES)
            num_games = 0

    # file = "qlearner.txt"
    # with open(file, 'w') as f:
    #     f.write(str(qlearner.q_values))
    # qlearner_100games = Q_learning_agent()
    # qlearner_100games.load_dict()
    # file = "qlearner_100.txt"
    # with open(file, 'w') as f:
    #     f.write(str(qlearner_100games.q_values))
    # print(filecmp.cmp("qlearner.txt", "qlearner_100.txt"))
