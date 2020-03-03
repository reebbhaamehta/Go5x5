import copy
import filecmp
import pickle
import sys
import time
import argparse
from my_player3 import Q_learning_agent
from game import Game
from read import readInput, readOutput
from write import writeOutput, writeNextInput
from random_player import RandomPlayer

X = 1
O = 2
TEST_GAMES = 100
GAME_SIZE = 5


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
        #  Play game as player1
        p1_stats, p2_stats = play_learn_track(go, game_number, player1, player2, p1_stats, p2_stats, batch)
        game_number += 1
        #  Play game as player2
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
        # print("player1 epsilon = {}".format(player1.epsilon))
        p1_stats[result] += 1
        if game_number % batch == 0:
            epsilon = player1.epsilon
            track_intelligence(1, p1_stats, batch, file, epsilon)
            p1_stats = [0, 0, 0]
    elif player2.learn:
        player2.update_Qvalues(go, num_game=game_number)
        # print("player2 epsilon = {}".format(player2.epsilon))
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
    qlearner.epsilon = 0
    qlearner.varyA_E = False
    if dict_number > 0:
        qlearner.load_dict(dict_number)
    battle(qlearner, random_player, int(qlearner.LEARN_GAMES), False)


def test():
    qlearner = Q_learning_agent()
    random_player = RandomPlayer()
    qlearner.learn = False
    qlearner.load_dict(500000)
    battle(random_player, qlearner, int(TEST_GAMES), True)
    battle(qlearner, random_player, int(TEST_GAMES), True)


# arbitrarily
def track_intelligence(pl_num, stats, batch, file, epsilon):
    # stats = [0, 0, 0] piece type of winner of the game (0 if it's a tie)
    stats = [round(x / batch * 100.0, 1) for x in stats]
    with open(file, 'a') as f:
        f.write(str(pl_num) + "," + ",".join([str(e) for e in stats]) + ',' + str(epsilon))
        f.write("\n")


# TODO: make an evaluation function that calculates win rate as a
#  metric to judge progress, this should happen while training and testing.
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num", type=int, help="Dictionary number to be loaded", default=-1)
    args = parser.parse_args()
    make_smarter(args.num)
    # test()
# TODO: check if update_qvalues is actually updating the correct
#  values and not just a random variable before throwing it away.
#  Checking briefly on Feb 27. I believe the q values are being
#  updated correctly. Passing is now explicit March 1st.

# TODO: implement my own functions and classes to account for
#  reading current / previous state and writing output files,
#  to check if the move I am about to make is valid and all
#  the helper functions that are required to check those conditions.

