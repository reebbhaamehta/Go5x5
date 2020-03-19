import time
import argparse
from LearnFromPlayedGames.learnfrombuffer import Q_learning_agent
from LearnFromPlayedGames.gamelearnbuffer import Game
from random_player import RandomPlayer
from Minimax import Minimax
import sys
from LearnFromPlayedGames.learnfrombuffer import GO_SIZE
from Minimax_old import Minimax_old
from Minimax_old2 import Minimax_old2

X = 1
O = 2
TEST_GAMES = 1
GAME_SIZE = GO_SIZE


def read_white_actions(game):

    pass


def read_black_actions(game):

    pass

def read_winner(game):

    pass


def make_smarter(dict_number):
    qlearner = Q_learning_agent()
    qlearner.alpha = 0.5
    qlearner.epsilon = 0.3
    qlearner.varyA_E = True
    total_games = int(qlearner.LEARN_GAMES)

    if dict_number > 0:
        qlearner.load_dict(dict_number)
    game_number = 0
    index = 0
    with open("games.txt", "r") as f:
        game_list = f.readline()
    game_list.strip("[").strip("]")
    print(game_list)
    for i in range(total_games + 1):
        game = game_list[index]
        print(game)
        exit()
        winner = read_winner(game)
        actions_white = read_white_actions(game)
        actions_black = read_black_actions(game)
        qlearner.self_actions = actions_black
        qlearner.opponent_actions = actions_white
        qlearner.update_Qvalues(winner, num_game=game_number)
        qlearner.update_Qvalues_opponent(winner)
        game_number += 1
        index += 1


def testQlearner(dict_num):
    qlearner = Q_learning_agent()
    random_player = RandomPlayer()
    minimax = Minimax_old2()
    qlearner_server = Q_learning_agent()
    if dict_num > 0:
        qlearner.fight(dict_num)
    dict_num = 10
    qlearner_server.fight(dict_num)
    # if dict_num > 0:
    #     qlearner.load_dict(dict_num)
    # player1: Player instance.always X
    # player2: Player instance.always O
    p1_stats = [0, 0, 0]
    p2_stats = [0, 0, 0]
    player1 = minimax
    player2 = qlearner_server
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--num", type=int, help="Dictionary number to be loaded", default=0)
    args = parser.parse_args()
    make_smarter(args.num)
    # testQlearner(args.num)
