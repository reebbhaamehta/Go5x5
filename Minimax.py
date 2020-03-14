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
DEPTH = 3


class Minimax:

    def __init__(self, side=None):
        self.side = side
        self.cache_max = {}
        self.cache_min = {}
        self.num_game = 0
        self.opponent = 1 if self.side == 2 else 2
        self.size = GO_SIZE

    def total_score(self, game, piece_type):
        """
        Get score of a player by counting the number of stones.

        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the game should end.
        """
        board = game.board
        count = 0
        count_opponent = 0
        liberties = 0
        liberty_list = []
        opponent_liberties = 0
        opponent_liberty_list = []
        opponents_as_neighbors = []
        if piece_type == 1:
            opponent = 2
        else:
            opponent = 1
        if board[2][2] == piece_type:
            count = count + 2
        for i in range(self.size):
            for j in range(self.size):
                # if I place a piece on the edges I get - 2 points
                if board[i][4] == self.side or \
                        board[j][4] == self.side or \
                        board[0][i] == self.side or \
                        board[0][j] == self.side:
                    count += -2
                # for every piece I have on the board I get two points
                if board[i][j] == self.side:
                    count += 2
                    liberty_list = []
                    ally_members = game.ally_dfs(i, j)
                    for member in ally_members:
                        neighbors = game.detect_neighbor(member[0], member[1])
                        for piece in neighbors:
                            # If there is empty space around a piece, it has liberty
                            if board[piece[0]][piece[1]] == 0:
                                if piece not in liberty_list:
                                    liberty_list.append(piece)
                                    count += 2
                            if board[piece[0]][piece[1]] == opponent:
                                if piece not in opponents_as_neighbors:
                                    opponents_as_neighbors.append(piece)
                                    count += 3
                    if not liberty_list:
                        count += -10
                    if len(liberty_list) == 1:
                        count += -10
                if board[i][j] == opponent:
                    count += -2
                    ally_members = game.ally_dfs(i, j)
                    for member in ally_members:
                        opponent_liberty_list = []
                        neighbors = game.detect_neighbor(member[0], member[1])
                        for piece in neighbors:
                            # If there is empty space around a piece, it has liberty
                            if board[piece[0]][piece[1]] == 0:
                                if piece not in opponent_liberty_list:
                                    opponent_liberty_list.append(piece)
                                    count += -2
                    if not opponent_liberty_list:
                        count += 20
                    if len(opponent_liberty_list) == 1:
                        count += 10


        if piece_type == 1:
            count = count - game.komi
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
                copy_board.next_board(2, 2, self.side, True)
                print("Minimax: piece_type = {}".format(self.side), \
                      "current board value = {}".format(self.total_score(copy_board, self.side)))
                return 2, 2
        if board.game_end():
            return
        else:
            # score, action = self._max(board)
            action = self.alpha_beta_cutoff_search(board, DEPTH)
            copy_board = copy.deepcopy(board)
            if action != "PASS":
                copy_board.next_board(action[0], action[1], self.side, True)
            print("Minimax: piece_type = {}".format(self.side), \
                  "current board value = {}".format(self.total_score(copy_board, self.side)))
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
            # random.shuffle(candidates)
            if not candidates:
                action = "PASS"
                v = max(v, min_value(board, alpha, beta, depth - 1))
                if v <= alpha:
                    return v
                alpha = max(alpha, v)
            else:
                for i, j in candidates:
                    copyBoard = copy.deepcopy(board)
                    copyBoard.next_board(i, j, self.side, False)
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
            # random.shuffle(candidates)
            if not candidates:
                action = "PASS"
                v = min(v, max_value(board, alpha, beta, depth - 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            else:
                for i, j in candidates:
                    copyBoard = copy.deepcopy(board)
                    valid = copyBoard.next_board(i, j, self.opponent, True)
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
        # random.shuffle(candidates)
        if not candidates:
            best_action = "PASS"
        else:
            for i, j in candidates:
                copyBoard = copy.deepcopy(board)
                copyBoard.next_board(i, j, self.side, True)
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
    game_piece_type, previous_board, current_board = go_game.read_input()
    go_game.set_board(game_piece_type, previous_board, current_board)
    player = Minimax()
    player.side = game_piece_type
    print(game_piece_type)
    # player.fight()
    next_action = player.get_input(go_game, game_piece_type)
    go_game.write_output(next_action)
