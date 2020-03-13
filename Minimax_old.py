import copy

# from Board import Board
import math
import pickle
import random

import numpy as np

from mygame import Game

WIN_REWARD = 1.0
DRAW_REWARD = 0.0
LOSS_REWARD = -1.0
GO_SIZE = 5


class Minimax_old:

    def __init__(self, side=None):
        self.side = side
        self.cache_max = {}
        self.cache_min = {}
        self.num_game = 0
        self.opponent = 1 if self.side == 2 else 2
        self.size = GO_SIZE
        self.learn = False


    def total_score(self, game, piece_type):
        """
        Get score of a player by counting the number of stones.

        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the game should end.
        """
        board = game.board
        count = 0
        count_opponent = 0
        if piece_type == 1:
            opponent = 2
        else:
            opponent = 1
        for i in range(self.size):
            for j in range(self.size):
                # if I place my piece in the center I get + 2 points
                if board[2][2] == piece_type:
                    count = count + 3
                # if I place a piece on the edges I get - 2 points
                if board[i][4] == piece_type or board[0][j] == piece_type:
                    count = count - 2
                # I get 1 point for each of my stones on the board
                if board[i][j] == piece_type:
                    count += 1
                    ally_members = game.ally_dfs(i, j)
                    for member in ally_members:
                        neighbors = game.detect_neighbor(member[0], member[1])
                        for piece in neighbors:
                        # If there is empty space around a piece, it has liberty
                            # I get + 2 points for each liberty I have
                            if board[piece[0]][piece[1]] == 0:
                                count += 2
                            # I get + 2 points if I place my stone near an opponents
                            if board[piece[0]][piece[1]] == opponent:
                                count += 2

        if piece_type == 1:
            count = count - game.komi
        #     self.opponent_score = self.score(2)
        # else:
        #     self.opponent_score = self.score(1)
        # if self.opponent_score < self.prev_opponent_score:
        #     count = count + 2
        return count

    def set_side(self, side):
        self.side = side
        self.opponent = 1 if self.side == 2 else 2

    def learn(self, board):
        pass

    def get_input(self, board: Game, piece_type):
        if board.score(piece_type) <= 0:
            self.side = piece_type
            self.opponent = 1 if self.side == 2 else 2
            if board.valid_place_check(2, 2, self.side, True):
                copy_board = copy.deepcopy(board)
                copy_board.place_chess(2, 2, self.side, True)
                # print("Minimax_old: piece_type = {}".format(self.side), \
                #       "current board value = {}".format(self.total_score(copy_board, self.side)))
                return 2, 2
        if board.game_end():
            return
        else:
            # score, action = self._max(board)
            action = self.alpha_beta_cutoff_search(board, 3)
            copy_board = copy.deepcopy(board)
            copy_board.place_chess(action[0], action[1], self.side, True)
            # print("Minimax_old: piece_type = {}".format(self.side), \
                  # "current board value = {}".format(self.total_score(copy_board, self.side)))
            return action  # board.move(action[0], action[1], self.side)

    def alpha_beta_cutoff_search(self, board, depth=4):

        def max_value(board, alpha, beta, depth):
            state = board.state_string()
            if depth == 0 or board.game_end():
                # board.visualize_board()
                return self.total_score(board, self.side)
            v = -np.inf
            candidates = []
            for i in range(board.size):
                for j in range(board.size):
                    if board.valid_place_check(i, j, self.side, test_check=True):
                        candidates.append((i, j))
            # print("Max candidates = {}".format(candidates))
            random.shuffle(candidates)
            if not candidates:
                action = "PASS"
                v = max(v, min_value(board, alpha, beta, depth - 1))
                if v <= alpha:
                    return v
                alpha = max(alpha, v)
            else:
                for i, j in candidates:
                    copyBoard = copy.deepcopy(board)
                    copyBoard.place_chess(i, j, self.side, False)
                    v = max(v, min_value(copyBoard, alpha, beta, depth - 1))
                    self.cache_max[state] = (v, (i, j))
                    # print("-"*60)
                    # print("Max candidates = {}".format((i, j, v)))
                    # board.visualize_board()
                    # copyBoard.visualize_board()
                    # print("-"*60)
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v

        def min_value(board, alpha, beta, depth):
            state = board.state_string()
            # if state in self.cache_min:
            # return self.cache_min[state][0]
            if depth == 0 or board.game_end():
                # board.visualize_board()
                return self.total_score(board, self.side)
            v = np.inf
            candidates = []
            for i in range(board.size):
                for j in range(board.size):
                    if board.valid_place_check(i, j, self.opponent, test_check=True):
                        candidates.append((i, j))
            random.shuffle(candidates)
            if not candidates:
                action = "PASS"
                v = min(v, max_value(board, alpha, beta, depth - 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            else:
                for i, j in candidates:
                    copyBoard = copy.deepcopy(board)
                    valid = copyBoard.place_chess(i, j, self.opponent, True)
                    if not valid:
                        raise ValueError("in min invalid move")
                    v = min(v, max_value(copyBoard, alpha, beta, depth - 1))
                    self.cache_min[state] = (v, (i, j))
                    # print("-"*60)
                    # print("Min candidates = {}".format((i, j, v)))
                    # board.visualize_board()
                    # copyBoard.visualize_board()
                    # print("-"*60)
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
            return v

        # self.load_dict_min()
        # self.load_dict_max()
        best_score = -np.inf
        beta = np.inf
        best_action = None
        candidates = []
        for i in range(board.size):
            for j in range(board.size):
                if board.valid_place_check(i, j, self.side, test_check=True):
                    candidates.append((i, j))
        random.shuffle(candidates)
        if not candidates:
            best_action = "PASS"
        else:
            for i, j in candidates:
                copyBoard = copy.deepcopy(board)
                copyBoard.place_chess(i, j, self.side, True)
                v = min_value(copyBoard, best_score, beta, depth)
                if v > best_score:
                    best_score = v
                    best_action = (i, j)
                    # print(best_action, best_score)
        # self.save_dict_max()
        # self.save_dict_min()
        return best_action

    def save_dict_max(self):
        pickle.dump(self.cache_max, open("cache_max.txt", "wb"))

    def save_dict_min(self):
        pickle.dump(self.cache_min, open("cache_min.txt", "wb"))

    def load_dict_min(self):
        try:
            self.cache_min = pickle.load(open("cache_min.txt", "rb"))
        except EOFError:
            self.cache_min = {}

    def load_dict_max(self):
        try:
            self.cache_max = pickle.load(open("cache_max.txt", "rb"))
        except EOFError:
            self.cache_max = {}

    def alt_heuristic(self, board, piece_type):
        if piece_type == 1:
            opponent = 2
        else:
            opponent = 1
        count_black = 0
        count_white = 2.5
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == 1:
                    count_black += 1
                elif board[i][j] == 2:
                    count_white += 1

        if piece_type == 1:
            diff = count_black - count_white
        else:
            diff = count_white - count_black
        return diff


if __name__ == "__main__":
    N = 5
    go_game = Game(N)
    game_piece_type, previous_board, board = go_game.read_input()
    go_game.set_board(game_piece_type, previous_board, board)
    player = Minimax_old()
    player.side = game_piece_type
    print(game_piece_type)
    # player.fight()
    next_action = player.get_input(go_game, game_piece_type)
    go_game.write_output(next_action)
