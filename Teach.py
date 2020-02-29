import copy
import filecmp
import pickle
import sys
import time

from my_player3 import Q_learning_agent
from host import GO, judge
from read import readInput, readOutput
from write import writeOutput, writeNextInput
from random_player import RandomPlayer

X = 1
O = 2
LEARN_GAMES = 1000000
TEST_GAMES = 100

"""
Learning:
- play game of go through the host
- against random player & then itself
- select best moves based on q value tables
- update Q values after each game
- update table of q values for each state
"""


def battle(player1, player2, iter, show_result=False):
    p1_stats = [0, 0, 0]  # draw, win, lose
    for i in range(iter + 1):
        go = GO(5)
        go.verbose = True
        go.init_board(5)
        result = go.play(player1, player2, True)
        batch = 100
        if player1.learn:
            player1.update_Qvalues(go)
            if i % 1000000 == 0:
                player1.save_dict(i)
        elif player2.learn:
            player2.update_Qvalues(go)
            if i % 1000000 == 0:
                player2.save_dict(i)
        if i % batch == 0:
            track_intelligence(p1_stats, batch)
            p1_stats = [0, 0, 0]
        p1_stats[result] += 1

    # p1_stats = [round(x / iter * 100.0, 1) for x in p1_stats]
    # if show_result:
    #     print('_' * 60)
    #     print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p1_stats[1], p1_stats[0],
    #                                                              p1_stats[2]).center(50))
    #     print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p1_stats[2], p1_stats[0],
    #                                                              p1_stats[1]).center(50))
    #     print('_' * 60)
    #     print()

    return p1_stats


def make_smarter():
    qlearner = Q_learning_agent()
    random_player = RandomPlayer()
    battle(random_player, qlearner, int(LEARN_GAMES), True)
    battle(qlearner, random_player, int(LEARN_GAMES), True)

    # qlearnerpoint2 = copy.deepcopy(qlearner)
    # qlearner.learn = False
    # battle(go, qlearnerpoint2, qlearner, int(LEARN_GAMES / 4), True)
    # battle(go, qlearner, qlearnerpoint2, int(LEARN_GAMES / 4), True)


def test():
    qlearner = Q_learning_agent()
    random_player = RandomPlayer()
    qlearner.learn = False
    qlearner.load_dict(1000000)
    battle(random_player, qlearner, int(TEST_GAMES), True)
    battle(qlearner, random_player, int(TEST_GAMES), True)


# arbitrarily
def track_intelligence(stats, batch):
    # stats = [0, 0, 0] piece type of winner of the game (0 if it's a tie)
    stats = [round(x / batch * 100.0, 1) for x in stats]

    with open("Track Intelligence.txt", 'a') as f:
        f.write(str(stats))
        f.write("\n")


# TODO: make an evaluation function that calculates win rate as a
#  metric to judge progress, this should happen while training and testing.
if __name__ == "__main__":
    make_smarter()
    # test()
    # TODO: check if update_qvalues is actually updating the correct
    #  values and not just a random variable before throwing it away.
    #  Checking briefly on Feb 27. I believe the q values are being
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
