import copy

import numpy as np
import gamelearnbuffer as go

if __name__ == "__main__":
    games20 = "games-20.txt"
    game_list = []
    with open(games20, "r") as f:
        lines = f.readlines()
        line_num = 0
        play_game = go.Game(5)
        self_piece_type = 0
        opponent_piece_type = 0
        state_action = []
        for line in lines:
            if line == "Black:TA White:You\n":
                self_piece_type = 2
                opponent_piece_type = 1
            elif line == "Black:You White:TA\n":
                self_piece_type = 1
                opponent_piece_type = 2

            if line == "Start Playing...\n":
                play_game = go.Game(5)
                play_game.new_board()
                state = play_game.state_string()
                play_game.visualize_board()
            if line == "Black makes move...\n":
                action = lines[line_num + 1].strip().split(",")
                if action == ["PASS"]:
                    action = "PASS"
                    play_game.previous_board = copy.deepcopy(play_game.board)

                else:
                    action = tuple(int(e) for e in action)
                    play_game.place_chess(action[0], action[1], 1, True)
                    play_game.died_pieces = play_game.remove_died_pieces(2)
                play_game.visualize_board()
                state_action.append((1, state, action))

            elif line == "White makes move...\n":
                action = lines[line_num + 1].strip().split(",")

                if action == ["PASS"]:
                    action = "PASS"
                    play_game.previous_board = copy.deepcopy(play_game.board)

                else:
                    action = tuple(int(e) for e in action)
                    play_game.place_chess(action[0], action[1], 2, True)
                    play_game.died_pieces = play_game.remove_died_pieces(1)
                play_game.visualize_board()
                state_action.append((2, state, action))

            state = play_game.state_string()

            if line == "White(You) win!\n":
                winner = self_piece_type
                print("O wins")
                game_list.append((winner, state_action))
                with open("games.txt", "a") as f:
                    f.writelines("{0},{1}\n" .format(winner, state_action))
            elif line == "Black(You) lose.\n":
                winner = opponent_piece_type
                game_list.append((winner, state_action))
                with open("games.txt", "a") as f:
                    f.writelines("{0},{1}\n" .format(winner, state_action))

            elif line == "Black(You) win!\n":
                winner = self_piece_type
                game_list.append((winner, state_action))
                print("X wins")
                with open("games.txt", "a") as f:
                    f.writelines("{0},{1}\n" .format(winner, state_action))

            elif line == "White(You) lose.\n":
                winner = opponent_piece_type
                game_list.append((winner, state_action))
                with open("games.txt", "a") as f:
                    f.writelines("{0},{1}\n" .format(winner, state_action))

            line_num += 1
