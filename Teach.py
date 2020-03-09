import copy
import filecmp
import pickle
import sys
import time
import argparse
from my_player3 import Q_learning_agent
from mygame import Game
from read import readInput, readOutput
from write import writeOutput, writeNextInput
from random_player import RandomPlayer
from Minimax import Minimax
import sys
from my_player3 import GO_SIZE

X = 1
O = 2
TEST_GAMES = 50
GAME_SIZE = GO_SIZE

"""
Learning:
- play game of go through the host
- against random player & then itself
- select best moves based on q value tables
- update Q values after each game
- update table of q values for each state
"""


# TODO: FIGURE OUT IF I CAN LEARN FROM THE OTHER PLAYERS MOVES
def battle(player1, player2, total_games, show_result=False):
    p1_stats = [0, 0, 0]  # draw, win, lose
    p2_stats = [0, 0, 0]
    timer = time.time()
    game_number = 0
    for i in range(total_games + 1):
        go = Game(GAME_SIZE)
        go.verbose = show_result
        go.new_board()
        batch = 100
        if game_number % int(total_games / 100) == 0:
            print('number of iterations = {}'.format(i))
            print('time = {}'.format(time.time() - timer))
            timer = time.time()
        p1_stats, p2_stats = play_learn_track(go, game_number, player1, player2, p1_stats, p2_stats, batch)
        game_number += 1
        go = Game(GAME_SIZE)
        go.verbose = show_result
        go.new_board()
        p1_stats, p2_stats = play_learn_track(go, game_number, player2, player1, p1_stats, p2_stats, batch)
        game_number += 1
    return


def play_learn_track(go, game_number, player1, player2, p1_stats, p2_stats, batch):
    result = go.play(player1, player2, True)
    file = "TrackInt.txt"
    if player1.learn:
        player1.update_Qvalues(go, num_game=game_number)
        p1_stats[result] += 1
        if game_number % batch == 0:
            epsilon = player1.epsilon
            track_intelligence(1, p1_stats, batch, file, epsilon)
            p1_stats = [0, 0, 0]
    elif player2.learn:
        player2.update_Qvalues(go, num_game=game_number)
        if result == 1:
            result = 2
        elif result == 2:
            result = 1
        p2_stats[result] += 1
        if game_number % batch == 1:
            epsilon = player2.epsilon
            track_intelligence(2, p2_stats, batch, file, epsilon)
            p2_stats = [0, 0, 0]
    return p1_stats, p2_stats


def make_smarter(dict_number):
    qlearner = Q_learning_agent()
    random_player = RandomPlayer()
    qlearner.alpha = 0.7
    qlearner.epsilon = 0.3
    qlearner.varyA_E = False
    if dict_number > 0:
        qlearner.load_dict(dict_number)
    battle(qlearner, random_player, int(qlearner.LEARN_GAMES), False)


def testMinimax():
    # qlearner = Q_learning_agent()
    random_player = RandomPlayer()
    minimax = Minimax()
    # qlearner.fight()
    # player1: Player instance.always X
    # player2: Player instance.always O
    p1_stats = [0, 0, 0]
    p2_stats = [0, 0, 0]
    player1 = minimax
    player2 = random_player
    for i in range(int(TEST_GAMES)):
        go = Game(GAME_SIZE)
        go.verbose = False
        go.new_board()
        result = go.play(player1, player2, False)
        p1_stats[result] += 1
    for i in range(int(TEST_GAMES)):
        go = Game(GAME_SIZE)
        go.verbose = False
        go.new_board()
        result = go.play(player2, player1, False)
        p2_stats[result] += 1

    print(p1_stats, p2_stats)
    p1_stats = [round(x / TEST_GAMES * 100.0, 1) for x in p1_stats]
    sys.stdout = open("Minimax_resutls.txt", "a")
    if True:
        print('_' * 60)
        print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p1_stats[1], p1_stats[0],
                                                                 p1_stats[2]).center(50))
        print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p1_stats[2], p1_stats[0],
                                                                 p1_stats[1]).center(50))
        print('_' * 60)
        print()
    p2_stats = [round(x / TEST_GAMES * 100.0, 1) for x in p2_stats]

    if True:
        print('_' * 60)
        print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p2_stats[1], p2_stats[0],
                                                                 p2_stats[2]).center(50))
        print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p2_stats[2], p2_stats[0],
                                                                 p2_stats[1]).center(50))
        print('_' * 60)
        print()
    # battle(random_player, qlearner, int(TEST_GAMES), True)
    # battle(qlearner, random_player, int(TEST_GAMES), True)


def testQlearner(dict_num):
    qlearner = Q_learning_agent()
    random_player = RandomPlayer()
    qlearner.fight(dict_num)
    # player1: Player instance.always X
    # player2: Player instance.always O
    p1_stats = [0, 0, 0]
    p2_stats = [0, 0, 0]
    player1 = qlearner
    player2 = random_player
    for i in range(int(TEST_GAMES)):
        go = Game(GAME_SIZE)
        go.verbose = False
        go.new_board()
        result = go.play(player1, player2, False)
        p1_stats[result] += 1
    # for i in range(int(TEST_GAMES)):
    #     go = Game(GAME_SIZE)
    #     go.verbose = False
    #     go.new_board()
    #     result = go.play(player2, player1, False)
    #     p2_stats[result] += 1

    print(p1_stats, p2_stats)
    p1_stats = [round(x / TEST_GAMES * 100.0, 1) for x in p1_stats]
    if True:
        print('_' * 60)
        print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p1_stats[1], p1_stats[0],
                                                                 p1_stats[2]).center(50))
        print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p1_stats[2], p1_stats[0],
                                                                 p1_stats[1]).center(50))
        print('_' * 60)
        print()
    # p2_stats = [round(x / TEST_GAMES * 100.0, 1) for x in p2_stats]
    #
    # if True:
    #     print('_' * 60)
    #     print('{:>15}(X) | Wins:{}% Draws:{}% Losses:{}%'.format(player2.__class__.__name__, p2_stats[1], p2_stats[0],
    #                                                              p2_stats[2]).center(50))
    #     print('{:>15}(O) | Wins:{}% Draws:{}% Losses:{}%'.format(player1.__class__.__name__, p2_stats[2], p2_stats[0],
    #                                                              p2_stats[1]).center(50))
    #     print('_' * 60)
    #     print()
    # battle(random_player, qlearner, int(TEST_GAMES), True)
    # battle(qlearner, random_player, int(TEST_GAMES), True)


# arbitrarily
def track_intelligence(pl_num, stats, batch, file, epsilon):
    # stats = [0, 0, 0] piece type of winner of the game (0 if it's a tie)
    stats = [round(x / batch * 100.0, 1) for x in stats]
    with open(file, 'a') as f:
        f.write(str(pl_num) + "," + ",".join([str(e) for e in stats]) + ',' + str(epsilon))
        f.write("\n")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--num", type=int, help="Dictionary number to be loaded", default=-1)
    # args = parser.parse_args()
    # make_smarter(args.num)
    # testQlearner(num)
    testMinimax()
# TODO: implement my own functions and classes to account for
#  reading current / previous state and writing output files,
#  to check if the move I am about to make is valid and all
#  the helper functions that are required to check those conditions.
