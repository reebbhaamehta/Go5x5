import copy
import numpy as np
import mygame as go
from Minimax import Minimax
import random


def evaluate_possibilities_board(go_game, player):
    m = Minimax(player)
    m.total_score(go_game, player)
    # print("-"*20)
    # print("From board: ")
    # print(go_game.visualize_board())
    # print("Obtain and evaluate the following ones: ")
    # candidates = []
    # for i in range(go_game.size):
    #     for j in range(go_game.size):
    #         if go_game.valid_place_check(i, j, m.side, test_check=True):
    #             candidates.append((i, j))
    # random.shuffle(candidates)
    # for c in candidates:
    #     new_board = go_game.make_copy()
    #     new_board.next_board(c[0], c[1], player, test_check=True)
    #     new_board.visualize_board()
    #     m.total_score(new_board, player, check_contributions=True)

if __name__ == "__main__":
    games20 = "LearnFromPlayedGames/29.txt"
    game_list = []
    n_move = 0
    with open(games20, "r") as f:
        lines = f.readlines()
        line_num = 0
        play_game = go.Game(5)
        self_piece_type = 0
        opponent_piece_type = 0
        state_action = []
        for line in lines:
            if line == "==Playing with random_player==\n":
                print(line)
            elif line == "==Playing with greedy_player==\n":
                print(line)
            elif line == "==Playing with aggressive_player==\n":
                print(line)
            if "=====Round " in line:
                print(line)
            if line == "Black:TA White:You\n":
                self_piece_type = 2
                print(line)
                opponent_piece_type = 1
            elif line == "Black:You White:TA\n":
                self_piece_type = 1
                opponent_piece_type = 2
                print(line)

            if line == "Start Playing...\n":
                play_game = go.Game(5)
                play_game.new_board()
                state = play_game.state_string()
                print(line)
                # play_game.visualize_board()
            player = -1
            if line == "Black makes move...\n":
                player = 1

            elif line == "White makes move...\n":
                player = 2

            if line == "Black makes move...\n" or line == "White makes move...\n":
                print(line)
                if not "ERROR" in line:
                    action_line = line_num +1
                else:
                    action_line = line_num +2

                action = lines[action_line].strip().split(",")

                if action == ["PASS"]:
                    action = "PASS"
                    play_game.previous_board = copy.deepcopy(play_game.board)

                else:
                    action = tuple(int(e) for e in action)
                    play_game.place_new_stone(action[0], action[1], player, True)
                    play_game.died_pieces = play_game.clean_dead_stones(3 - player)
                play_game.visualize_board()
                state_action.append((player, state, action))
                evaluate_possibilities_board(play_game, player)
                n_move += 1
                print(n_move)


            state = play_game.state_string()

            if line == "White(You) win!\n":
                winner = self_piece_type
                print(line)
                game_list.append((winner, state_action))
                with open("games.txt", "a") as f:
                    f.writelines("{0},{1}\n" .format(winner, state_action))
            elif line == "Black(You) lose.\n":
                print(line)
                winner = opponent_piece_type
                game_list.append((winner, state_action))
                with open("games.txt", "a") as f:
                    f.writelines("{0},{1}\n" .format(winner, state_action))

            elif line == "Black(You) win!\n":
                winner = self_piece_type
                game_list.append((winner, state_action))
                print(line)
                with open("games.txt", "a") as f:
                    f.writelines("{0},{1}\n" .format(winner, state_action))

            elif line == "White(You) lose.\n":
                winner = opponent_piece_type
                print(line)
                game_list.append((winner, state_action))
                with open("games.txt", "a") as f:
                    f.writelines("{0},{1}\n" .format(winner, state_action))

            line_num += 1