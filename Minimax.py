import copy

# from Board import Board
import math

import numpy as np

from game import Game

WIN_REWARD = 1.0
DRAW_REWARD = 0.0
LOSS_REWARD = -1.0


class Minimax:

    def __init__(self, side=None):
        self.side = side
        self.cache_max = {}
        self.cache_min = {}
        self.num_game = 0
        self.opponent = 1 if self.side == 2 else 2

    def set_side(self, side):
        self.side = side
        self.opponent = 1 if self.side == 2 else 2

    def learn(self, board):
        pass

    def get_input(self, board: Game, piece_type):
        if self.side != piece_type and board.score(piece_type) <= 0:
            self.side = piece_type
            self.opponent = 1 if self.side == 2 else 2
        if board.game_end():
            return
        else:
            # score, action = self._max(board)
            action = self.alpha_beta_cutoff_search(board, 4)
            return action  # board.move(action[0], action[1], self.side)

    def alpha_beta_cutoff_search(self, board, depth=4):

        def max_value(board, alpha, beta, depth):
            if depth == 0 or board.game_end():
                # board.visualize_board()
                # print(depth)
                return board.total_score(self.side)
            v = -np.inf
            candidates = []
            for i in range(board.size):
                for j in range(board.size):
                    if board.valid_place_check(i, j, self.side, test_check=True):
                        candidates.append((i, j))
            # print("Max candidates = {}".format(candidates))
            if not candidates:
                action = "PASS"
                v = max(v, min_value(board, alpha, beta, depth - 1))
                if v <= alpha:
                    return v
                alpha = max(alpha, v)
            else:
                for i, j in candidates:
                    copyBoard = copy.deepcopy(board)
                    copyBoard.place_chess(i, j, self.side, True)
                    v = max(v, min_value(copyBoard, alpha, beta, depth - 1))
                    print("-"*60)
                    print("Max candidates = {}".format((i, j, v)))
                    board.visualize_board()
                    copyBoard.visualize_board()
                    print("-"*60)
                    if v >= beta:
                        return v
                    alpha = max(alpha, v)
            return v

        def min_value(board, alpha, beta, depth):
            if depth == 0 or board.game_end():
                # board.visualize_board()
                return board.total_score(self.side)
            v = np.inf
            candidates = []
            for i in range(board.size):
                for j in range(board.size):
                    if board.valid_place_check(i, j, self.opponent, test_check=True):
                        candidates.append((i, j))

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
                    print("-"*60)
                    print("Min candidates = {}".format((i, j, v)))
                    board.visualize_board()
                    copyBoard.visualize_board()
                    print("-"*60)
                    if v <= alpha:
                        return v
                    beta = min(beta, v)
            return v

        best_score = -np.inf
        beta = np.inf
        best_action = None
        candidates = []
        for i in range(board.size):
            for j in range(board.size):
                if board.valid_place_check(i, j, self.side, test_check=True):
                    candidates.append((i, j))
        # print("ABP candidates = {}".format(candidates))

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
        return best_action

    # def _min(self, board: Game):
    #     state = board.state_string()
    #     if state in self.cache_min:
    #         return self.cache_min[state]
    #     elif board.game_end() and board.judge_winner() == 0:
    #         return board.total_score(self.side), None
    #     elif board.game_end() and board.judge_winner() == self.side:
    #         return board.total_score(self.side), None
    #     elif board.game_end() and board.judge_winner() == self.opponent:
    #         return board.total_score(self.side), None
    #     else:
    #         min_value, action = board.score(self.side), None
    #         candidates = []
    #         for i in range(board.size):
    #             for j in range(board.size):
    #                 if board.valid_place_check(i, j, self.opponent, test_check=True):
    #                     candidates.append((i, j))
    #                 # candidates.append("PASS")
    #         # candidates = [(i, j) for i in range(3) if board.state[i][j] == 0 for j in iter(range(3))]
    #         for i, j in candidates:
    #             copyBoard = copy.deepcopy(board)
    #             copyBoard.place_chess(i, j, self.opponent, True)
    #             score, a = self._max(copyBoard)
    #             if score < min_value or action is None:
    #                 min_value, action = score, (i, j)
    #             self.cache_min[state] = (min_value, action)
    #         # print("MIN NODE = {}".format(min_value), "state = {}".format(state))
    #         return min_value, action
    #
    # def _max(self, board):
    #     state = board.state_string()
    #     if state in self.cache_max:
    #         return self.cache_max[state]
    #     elif board.game_end() and board.judge_winner() == 0:
    #         return board.total_score(self.side), None
    #     elif board.game_end() and board.judge_winner() == self.side:
    #         return board.total_score(self.side), None
    #     elif board.game_end() and board.judge_winner() == self.opponent:
    #         return board.total_score(self.side), None
    #     else:
    #         max_value, action = board.score(self.side), None
    #         candidates = []
    #         for i in range(board.size):
    #             for j in range(board.size):
    #                 if board.valid_place_check(i, j, self.side, test_check=True):
    #                     candidates.append((i, j))
    #                 # candidates.append("PASS")
    #         # candidates = [(i, j) for i in range(3) if board.state[i][j] == 0 for j in iter(range(3))]
    #         for i, j in candidates:
    #             b = copy.deepcopy(board)
    #             b.place_chess(i, j, self.side, True)
    #             score, a = self._min(b)
    #             if score > max_value or action is None:
    #                 max_value, action = score, (i, j)
    #             self.cache_max[state] = (max_value, action)
    #         # print("MAX NODE = {}".format(max_value), "state = {}".format(state))
    #         return max_value, action


if __name__ == "__main__":
    N = 5
    go_game = Game(N)

    game_piece_type, previous_board, board = go_game.read_input()
    go_game.set_board(game_piece_type, previous_board, board)
    player = Minimax()
    player.side = game_piece_type
    print(game_piece_type)
    # player.fight()
    next_action = player.get_input(go_game, game_piece_type)
    go_game.write_output(next_action)
