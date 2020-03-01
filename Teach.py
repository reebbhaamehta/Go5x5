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
LEARN_GAMES = 10 ** 6
TEST_GAMES = 100

"""
Learning:
- play game of go through the host
- against random player & then itself
- select best moves based on q value tables
- update Q values after each game
- update table of q values for each state
"""


# TODO: FIGURE OUT IF I CAN LEARN FROM THE OTHER PLAYERS MOVES
def battle(player1, player2, iter, show_result=False):
    p1_stats = [0, 0, 0]  # draw, win, lose
    p2_stats = [0, 0, 0]
    timer = time.time()
    for i in range(iter + 1):
        go = GO(5)
        go.verbose = False
        go.init_board(5)
        result_p1 = go.play(player1, player2, True)
        result_p2 = go.play(player2, player1, True)
        batch = 100
        if i % int(iter / 100) == 0:
            print('number of iterations = {}'.format(i))
            print('time = {}'.format(time.time() - timer))
            timer = time.time()
        if player1.learn:
            player1.update_Qvalues(go, num_game=i)

        elif player2.learn:
            player2.update_Qvalues(go, num_game=i)

        if i % batch == 0:
            file = "TrackIntP1.txt"
            track_intelligence(p1_stats, batch, file)
            # file = "TrackIntP2.txt"
            p2_stats = [p2_stats[0], p2_stats[2], p2_stats[1]] # p2 stats as player one would see it.
            track_intelligence(p2_stats, batch, file)
            p1_stats = [0, 0, 0]
            p2_stats = [0, 0, 0]
        p1_stats[result_p1] += 1
        p2_stats[result_p2] += 1

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
    battle(qlearner, random_player, int(qlearner.LEARN_GAMES), True)
    # battle(qlearner, random_player, int(LEARN_GAMES), True)
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
def track_intelligence(stats, batch, file):
    # stats = [0, 0, 0] piece type of winner of the game (0 if it's a tie)
    stats = [round(x / batch * 100.0, 1) for x in stats]

    with open(file, 'a') as f:
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
