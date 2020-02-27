import copy
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
LEARN_GAMES = 10000000

"""
Learning:
- play game of go through the host
- against random player & then itself
- select best moves based on q value tables
- update Q values after each game
- update table of q values for each state
"""


def battle(go, player1, player2, iter, show_result=False):
    p1_stats = [0, 0, 0]  # draw, win, lose
    for i in range(0, iter):
        go.init_board(5)
        result = go.play(player1, player2, False)
        if player1.learn:
            player1.update_Qvalues(go, i)
            if i % 100000 == 0:
                player1.save_dict(i)
        elif player2.learn:
            player2.update_Qvalues(go, i)
            if i % 100000 == 0:
                player2.save_dict(i)
        p1_stats[result] += 1

    p1_stats = [round(x / iter * 100.0, 1) for x in p1_stats]
    if show_result:
        print('_' * 60)
        print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p1_stats[1], p1_stats[0],
                                                                 p1_stats[2]).center(50))
        print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p1_stats[2], p1_stats[0],
                                                                 p1_stats[1]).center(50))
        print('_' * 60)
        print()

    return p1_stats


if __name__ == "__main__":
    qlearner = Q_learning_agent()
    random_player = RandomPlayer()
    go = GO(5)
    battle(go, random_player, qlearner, int(LEARN_GAMES / 4), True)
    battle(go, qlearner, random_player, int(LEARN_GAMES / 4), True)

    qlearnerpoint2 = Q_learning_agent()
    qlearnerpoint2 = copy.deepcopy(qlearner)
    qlearner.learn = False
    battle(go, qlearnerpoint2, qlearner, int(LEARN_GAMES / 4), True)
    battle(go, qlearner, qlearnerpoint2, int(LEARN_GAMES / 4), True)

    # TODO: check if update_qvalues is actually updating the correct
    #  values and not just a random variable before throwing it away.
    #  Checking breifly on Feb 27. I believe the q values are being
    #  updated correctly.

    # TODO: implement my own functions and classes to account for
    #  reading current / previous state and writing output files,
    #  to check if the move I am about to make is valid and all
    #  the helper functions that are required to check those conditions.

    # file = "qlearner.txt"
    # with open(file, 'w') as f:
    #     f.write(str(qlearner.q_values))
    # qlearner_100games = Q_learning_agent()
    # qlearner_100games.load_dict()
    # file = "qlearner_100.txt"
    # with open(file, 'w') as f:
    #     f.write(str(qlearner_100games.q_values))
    # print(filecmp.cmp("qlearner.txt", "qlearner_100.txt"))
