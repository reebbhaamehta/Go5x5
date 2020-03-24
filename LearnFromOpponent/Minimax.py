# 7042208305 :Reebbhaa Mehta

import copy
import math
import pickle
import random

import numpy

from gamelearnopponent import Game

WIN_REWARD = 1.0
DRAW_REWARD = 0.0
LOSS_REWARD = -1.0
GO_SIZE = 5
DEPTH = 1


class Minimax:

    def __init__(self, side=None):
        self.side = side
        self.cache = {}
        self.num_game = 0
        self.opponent = 1 if self.side == 2 else 2
        self.size = GO_SIZE
        self.learn = False

    def total_score(self, game, piece_type):
        """
        Get score of a player by counting the number of stones.

        :param game:
        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the game should end.
        """
        board = game.board
        count = 0
        #  weights
        self_weight = 1
        opponent_weight = 1
        center_weight = 1
        liberty_weight = 500
        opponent_liberty_weight = 500
        self_edge_weight = 7
        opponent_edge_weight = 7
        chain_weight = 5
        opponent_chain_weight = 5
        total_liberty_weight = 5
        total_opponent_liberty_weight = 5
        self_corner_weight = 10
        opponent_corner_weight = 10

        if piece_type == 1:
            count = count - game.komi
            opponent = 2
        else:
            opponent = 1

        if game.game_end():
            # game.visualize_board()
            if game.judge_winner() == piece_type:
                return 10 ** 4  # game.score(piece_type) + count
            elif game.judge_winner() == opponent:
                return -10 ** 4
        liberty_array = numpy.zeros((game.size, game.size), dtype=bool)
        opponent_liberty_array = numpy.zeros((game.size, game.size), dtype=bool)

        if board[2][2] == piece_type:
            count = count + center_weight

        for i in range(self.size):
            for j in range(self.size):
                # for every piece I have on the board I get two points
                chain = []
                if board[i][j] == self.side:
                    count += self_weight
                    chain = game.ally_dfs(i, j)
                    neighbors = game.detect_neighbor(i, j)
                    for piece in neighbors:
                        # If there is empty space around a piece, it has liberty
                        if board[piece[0]][piece[1]] == 0:
                            liberty_array[piece[0]][piece[1]] = True
                    if not numpy.any(liberty_array):
                        count += -liberty_weight
                opponent_chain = []
                if board[i][j] == opponent:
                    count += -opponent_weight
                    opponent_chain = game.ally_dfs(i, j)
                    neighbors = game.detect_neighbor(i, j)
                    for piece in neighbors:
                        # If there is empty space around a piece, it has liberty
                        if board[piece[0]][piece[1]] == 0:
                            opponent_liberty_array[piece[0]][piece[1]] = True
                    if not numpy.any(opponent_liberty_array):
                        count += opponent_liberty_weight
                if i == 0 or i == 4 or j == 0 or j == 4:  # on the sides
                    if board[i][j] == self.side:
                        count += -self_edge_weight
                    if board[i][j] == self.opponent and (i, j) in opponent_chain \
                            and len(opponent_chain) > 2:
                        count += opponent_edge_weight
                if (i, j) == (0, 0) or (i, j) == (4, 4) or (i, j) == (0, 4) or (i, j) == (4, 0):
                    if board[i][j] == self.side:
                        count += -self_corner_weight
                    # if board[i][j] == self.opponent:
                    #     count += opponent_corner_weight
                count += -numpy.sqrt(len(opponent_chain)) * chain_weight
                count += numpy.sqrt(len(chain)) * opponent_chain_weight

        count += numpy.sum(liberty_array) * total_liberty_weight
        count += -numpy.sum(opponent_liberty_array) * total_opponent_liberty_weight
        return count

    def set_side(self, side):
        self.side = side
        self.opponent = 1 if self.side == 2 else 2

    def learn(self, board):
        pass

    def aggressive_action(self, go, piece_type):
        pass

    def get_input(self, go: Game, piece_type):
        self.load_dict()
        # print(board.n_move)
        go.visualize_board()
        if go.score(piece_type) <= 0:
            self.side = piece_type
            self.opponent = 1 if self.side == 2 else 2
            self.cache = {}
            open("cache.txt", "w").close()
            if go.valid_place_check(2, 2, self.side, True):
                copy_board = copy.deepcopy(go)
                copy_board.next_board(2, 2, self.side, True)
                # print("Minimax: piece_type = {}".format(self.side), \
                #       "current board value = {}".format(self.total_score(copy_board, self.side)))
                return 2, 2
        if go.game_end():
            return
        else:
            # score, action = self._max(board)
            depth = DEPTH
            if go.n_move > 18:
                depth = 24 - go.n_move
            elif go.n_move < 8:
                # return aggressive_action(go, piece_type)
                depth = 1
            action = self.alpha_beta_cutoff_search(go, depth)
            copy_board = copy.deepcopy(go)
            if action != "PASS":
                # print(action)
                copy_board.next_board(action[0], action[1], self.side, True)
            # print("Minimax: piece_type = {}".format(self.side), \
            #       "current board value = {}".format(self.total_score(copy_board, self.side)))

            self.save_dict()
            return action  # board.move(action[0], action[1], self.side)

    def alpha_beta_cutoff_search(self, go: Game, depth=4):

        def max_value(board, alpha, beta, depth):
            state = board.state_string()
            if depth == 0 or board.game_end():
                if state in self.cache:
                    return self.cache[state]
                return self.total_score(board, self.side)
            v_max = -numpy.inf
            candidates = []
            for i in range(board.size):
                for j in range(board.size):
                    if board.valid_place_check(i, j, self.side, test_check=True):
                        candidates.append((i, j))
            random.shuffle(candidates)
            if not candidates:
                action = "PASS"
                v_max = max(v_max, min_value(board, alpha, beta, depth - 1))
                if v_max <= alpha:
                    return v_max
                alpha = max(alpha, v_max)
            else:
                for i, j in candidates:
                    copyBoard = copy.deepcopy(board)
                    copyBoard.next_board(i, j, self.side, False)
                    copyBoard.n_move += 1
                    v_max = max(v_max, min_value(copyBoard, alpha, beta, depth - 1))
                    if v_max is not None:
                        self.cache[state] = v_max
                    if v_max >= beta:
                        return v_max
                    alpha = max(alpha, v_max)
            return v_max

        def min_value(board, alpha, beta, depth):
            state = board.state_string()
            if depth == 0 or board.game_end():
                if state in self.cache:
                    return self.cache[state]
                return self.total_score(board, self.side)
            v_min = numpy.inf
            candidates = []
            for i in range(board.size):
                for j in range(board.size):
                    if board.valid_place_check(i, j, self.opponent, test_check=True):
                        candidates.append((i, j))
            random.shuffle(candidates)
            if not candidates:
                action = "PASS"
                v_min = min(v_min, max_value(board, alpha, beta, depth - 1))
                if v_min <= alpha:
                    return v_min
                beta = min(beta, v_min)
            else:
                for i, j in candidates:
                    copyBoard = copy.deepcopy(board)
                    valid = copyBoard.next_board(i, j, self.opponent, True)
                    copyBoard.n_move += 1
                    if not valid:
                        raise ValueError("in min invalid move")
                    v_min = min(v_min, max_value(copyBoard, alpha, beta, depth - 1))
                    if v_min is not None:
                        self.cache[state] = v_min
                    if v_min <= alpha:
                        return v_min
                    beta = min(beta, v_min)
            return v_min

        best_score = -numpy.inf
        beta = numpy.inf
        best_action = None
        candidates = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, self.side, test_check=True):
                    candidates.append((i, j))
        random.shuffle(candidates)
        if not candidates:
            best_action = "PASS"
        else:
            for i, j in candidates:
                copyBoard = copy.deepcopy(go)
                copyBoard.next_board(i, j, self.side, True)
                copyBoard.n_move += 1
                if go.n_move < 8:
                    value = max_value(copyBoard, best_score, beta, depth)
                else:
                    value = min_value(copyBoard, best_score, beta, depth)
                if value > best_score:
                    best_score = value
                    best_action = (i, j)
        return best_action

    def save_dict(self):
        pickle.dump(self.cache, open("cache.txt", "wb"))

    def load_dict(self):
        try:
            self.cache = pickle.load(open("cache.txt", "rb"))
        except EOFError:
            self.cache = {}
        except FileNotFoundError:
            self.cache = {}

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
    game_piece_type, previous_board, current_board, go_game.n_move = go_game.read_input()
    go_game.set_board(game_piece_type, previous_board, current_board)
    player = Minimax()
    if go_game.new_game:
        player.cache = {}
        open("cache.txt", "w").close()
    player.side = game_piece_type
    next_action = player.get_input(go_game, game_piece_type)
    go_game.n_move += 2

    go_game.write_output(next_action)
