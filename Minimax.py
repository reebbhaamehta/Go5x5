# 7042208305 :Reebbhaa Mehta

import copy
import math
import pickle
import random

import numpy

from mygame import Game

WIN_REWARD = 1.0
DRAW_REWARD = 0.0
LOSS_REWARD = -1.0
GO_SIZE = 5
DEPTH = 3

WEIGHTS = {1: {"self_w":40, "center_w": 1, "libert_w": 2, "self_edge_w": 7, "chain_weight": 1, "total_liberty_w": 5,
            "corner_weight": 1, "virtual_liberties_weight": 2, "win_score": 10**3},
            2: {"self_w":10, "center_w": 1, "libert_w": 2, "self_edge_w": 7, "chain_weight": 5, "total_liberty_w": 5,
            "corner_weight": 1, "virtual_liberties_weight": 2, "win_score": 10**3}}

class Minimax:
    def __init__(self, side=1, self_w=10, center_w=1, libert_w=2, self_edge_w=7, chain_weight=1, total_liberty_w=5, 
            corner_weight=1, virtual_liberties_weight=2, win_score=10**3):
        self.identity = side
        self.cache = {}
        self.num_game = 0
        self.opponent = 1 if self.identity == 2 else 2
        self.size = GO_SIZE
        self.learn = False

        #  weights
        self.self_weight                = WEIGHTS[side]["self_w"]
        self.opponent_weight            = WEIGHTS[side]["self_w"]
        self.center_weight              = WEIGHTS[side]["center_w"]
        self.liberty_weight             = WEIGHTS[side]["libert_w"]
        self.opponent_liberty_weight    = WEIGHTS[side]["libert_w"]
        self.self_edge_weight           = WEIGHTS[side]["self_edge_w"]
        self.opponent_edge_weight       = WEIGHTS[side]["self_edge_w"]
        self.chain_weight               = WEIGHTS[side]["chain_weight"]
        self.opponent_chain_weight      = WEIGHTS[side]["chain_weight"]
        self.virtual_liberties_weight   = WEIGHTS[side]["virtual_liberties_weight"]
        self.opponent_virtual_liberties_weight = WEIGHTS[side]["virtual_liberties_weight"]
        self.total_liberty_weight       = WEIGHTS[side]["total_liberty_w"]
        self.self_corner_weight         = WEIGHTS[side]["corner_weight"]
        self.total_opponent_liberty_weight = WEIGHTS[side]["total_liberty_w"]
        self.win_score                  = WEIGHTS[side]["win_score"]

    def total_score(self, game, piece_type, check_contributions=False):
        """
        Get score of a player by counting the number of stones.

        :param game:
        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the game should end.
        """
        board = game.board
        count = 0
        contributions = {}

        if piece_type == 1:
            count = count - game.komi
            opponent = 2
        else:
            opponent = 1

        contributions["komi"] = count
        contributions["chain"] = 0
        contributions["opponent_chain"] = 0
        contributions["self"] = 0
        contributions["opponent"] = 0
        contributions["virtual_liberties"] = 0
        contributions["opponent_virtual_liberties"] = 0
        contributions["liberty_array"] = 0
        contributions["opponent_liberty_array"] = 0
        contributions["edge_weight"] = 0
        contributions["corner_weight"] = 0
        contributions["liberty"] = 0
        contributions["opponent_liberty"] = 0
        contributions["opponent_edge"] = 0

        # print(game.game_end(), game.n_move)
        if game.is_game_finished():
            # game.visualize_board()
            if game.and_the_winner_is___() == piece_type:
                count += self.win_score # game.score(piece_type) + count
                contributions["win_bonus"] = self.win_score
            elif game.and_the_winner_is___() == opponent:
                count += -self.win_score
                contributions["win_bonus"] = -self.win_score
        liberty_array = numpy.zeros((game.size, game.size), dtype=bool)
        opponent_liberty_array = numpy.zeros((game.size, game.size), dtype=bool)
        virtual_liberties, opponent_virtual_liberties = 0, 0


        if board[2][2] == piece_type:
            count = count + self.center_weight
            contributions["center"] = self.center_weight

        for i in range(self.size):
            for j in range(self.size):
                # for every piece I have on the board I get two points
                chain = []
                if board[i][j] == self.identity:
                    count += self.self_weight
                    contributions["self"] += self.self_weight
                    chain = game.ally_dfs(i, j)
                    neighbors = game.gimme_adjacent(i, j)
                    for piece in neighbors:
                        # If there is empty space around a piece, it has liberty
                        if board[piece[0]][piece[1]] == 0:
                            virtual_liberties += 1
                            liberty_array[piece[0]][piece[1]] = True
                    if not numpy.any(liberty_array):
                        count += self.liberty_weight
                        contributions["liberty"] += self.liberty_weight
                opponent_chain = []
                if board[i][j] == opponent:
                    count += -self.opponent_weight
                    contributions["opponent"] += -self.opponent_weight
                    opponent_chain = game.ally_dfs(i, j)
                    neighbors = game.gimme_adjacent(i, j)
                    for piece in neighbors:
                        # If there is empty space around a piece, it has liberty
                        if board[piece[0]][piece[1]] == 0:
                            opponent_virtual_liberties += 1
                            opponent_liberty_array[piece[0]][piece[1]] = True
                    if not numpy.any(opponent_liberty_array):
                        count += -self.opponent_liberty_weight
                        contributions["opponent_liberty"] += -self.opponent_liberty_weight
                if i == 0 or i == 4 or j == 0 or j == 4:  # on the sides
                    if board[i][j] == self.identity:
                        count += -self.self_edge_weight
                        contributions["edge_weight"] += -self.self_edge_weight
                    if board[i][j] == self.opponent and (i, j) in opponent_chain \
                            and len(opponent_chain) > 2:
                        count += -self.opponent_edge_weight
                        contributions["opponent_edge"] += -self.opponent_edge_weight
                if (i, j) == (0, 0) or (i, j) == (4, 4) or (i, j) == (0, 4) or (i, j) == (4, 0):
                    if board[i][j] == self.identity:
                        count += -self.self_corner_weight
                        contributions["corner_weight"] += -self.self_corner_weight
                    # if board[i][j] == self.opponent:
                    #     count += opponent_corner_weight
                count += numpy.sqrt(len(chain)) * self.chain_weight
                count += -numpy.sqrt(len(opponent_chain)) * self.opponent_chain_weight
                contributions["chain"] += numpy.sqrt(len(chain)) * self.chain_weight
                contributions["opponent_chain"] += -numpy.sqrt(len(opponent_chain)) * self.opponent_chain_weight

        count += -opponent_virtual_liberties * self.opponent_virtual_liberties_weight
        contributions["opponent_virtual_liberties"] = -opponent_virtual_liberties * self.opponent_virtual_liberties_weight
        count += numpy.sum(liberty_array) * self.total_liberty_weight
        contributions["liberty_array"] = numpy.sum(liberty_array) * self.total_liberty_weight
        count += -numpy.sum(opponent_liberty_array) * self.total_opponent_liberty_weight
        contributions["opponent_liberty_array"] = -numpy.sum(opponent_liberty_array) * self.total_opponent_liberty_weight
        if check_contributions:
            count2 = 0
            for e in contributions:
                print(e, contributions[e])
                count2 += contributions[e]
            print("{} =?= {}".format(count, count2))
        # game.visualize_board()
        # print(count)
        return count

    def set_side(self, side):
        self.identity = side
        self.opponent = 1 if self.identity == 2 else 2

    def learn(self, board):
        pass

    def aggressive_action(self, go, piece_type):
        pass

    def get_input(self, go: Game, piece_type):
        if self.identity is None:
            self.identity = piece_type
        elif self.identity != piece_type:
            self.identity = piece_type
        else:
            self.__init__(piece_type)
        self.load_dict()
        # print(board.n_move)
        go.visualize_board()
        if go.count_player_stones(piece_type) <= 0:
            self.identity = piece_type
            self.opponent = 1 if self.identity == 2 else 2
            self.cache = {}
            open("cache.txt", "w").close()
            if go.is_position_valid(2, 2, self.identity, True):
                copy_board = go.make_copy()
                copy_board.next_board(2, 2, self.identity, True)
                # print("Minimax: piece_type = {}".format(self.side), \
                #       "current board value = {}".format(self.total_score(copy_board, self.side)))
                return 2, 2
        if go.is_game_finished():
            return
        else:
            # score, action = self._max(board)
            depth = DEPTH
            action = self.alpha_beta_adaptive_agent(go, depth)
            copy_board = go.make_copy()
            if action != "PASS":
                # print(action)
                copy_board.next_board(action[0], action[1], self.identity, True)
            # print("Minimax: piece_type = {}".format(self.side), \
            #       "current board value = {}".format(self.total_score(copy_board, self.side)))

            self.save_dict()
            return action  # board.move(action[0], action[1], self.side)

    def alpha_beta_adaptive_agent(self, go: Game, depth=4):

        def max_value(board, alpha, beta, depth):
            if depth == 0 or board.is_game_finished():
                state = board.state_string()
                if state in self.cache:
                    return self.cache[state]
                return self.total_score(board, self.identity)
            v_max = -numpy.inf
            candidates = []
            for i in range(board.size):
                for j in range(board.size):
                    if board.is_position_valid(i, j, self.identity, test_check=True):
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
                    poss_max_board = board.make_copy()
                    poss_max_board.next_board(i, j, self.identity, False)
                    poss_max_board.n_move += 1
                    v_max = max(v_max, min_value(poss_max_board, alpha, beta, depth - 1))
                    if v_max is not None:
                        state = board.state_string()
                        self.cache[state] = v_max
                    if v_max >= beta:
                        return v_max
                    alpha = max(alpha, v_max)
            return v_max

        def min_value(board, alpha, beta, depth):
            if depth == 0 or board.is_game_finished():
                state = board.state_string()
                if state in self.cache:
                    return self.cache[state]
                return self.total_score(board, self.identity)
            v_min = numpy.inf
            candidates = []
            for i in range(board.size):
                for j in range(board.size):
                    if board.is_position_valid(i, j, self.opponent, test_check=True):
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
                    poss_min_board = board.make_copy()
                    valid = poss_min_board.next_board(i, j, self.opponent, True)
                    poss_min_board.n_move += 1
                    if not valid:
                        raise ValueError("in min invalid move")
                    v_min = min(v_min, max_value(poss_min_board, alpha, beta, depth - 1))
                    if v_min is not None:
                        state = board.state_string()
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
                if go.is_position_valid(i, j, self.identity, test_check=True):
                    candidates.append((i, j))
        random.shuffle(candidates)
        if go.n_move < 6:
            depth = 0
        elif go.n_move < 10:
            depth = 2
        elif len(candidates) < 24 - 18:
            depth = len(candidates)
        if not candidates:
            best_action = "PASS"
        else:
            for i, j in candidates:
                possible_board = go.make_copy()
                possible_board.next_board(i, j, self.identity, True)
                possible_board.n_move += 1
                value = min_value(possible_board, best_score, beta, depth)
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
    player = Minimax(game_piece_type)
    if go_game.new_game:
        player.cache = {}
        open("cache.txt", "w").close()
    next_action = player.get_input(go_game, game_piece_type)
    go_game.n_move += 2

    go_game.write_output(next_action)
