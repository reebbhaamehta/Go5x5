import copy
import math
import random

from game import Game

WIN = 1.0
DRAW = 0.0
LOSS = -1.0
MIN_SCORE = -math.inf
MAX_SCORE = math.inf



class MiniMax:

    def __init__(self):
        self.identity = None
        self.opponent = None
        self.board = ""
        self.previous_board = ""
        self.max_depth = 4
        self.nodes = {}


    def set_player(self, side):
        self.identity = side
        self.opponent =

    def current_state(self, game):
        self.board = game.state_string("Current")

    def previous_state(self, game):
        self.previous_board = game.state_string("Previous")

    def cutoff_test(self, state, depth):
        return True

    def eval_fn(self, game, side):
        return game.score(side)

    def successors(self, state):

    def max(self, game, alpha, beta, depth):
        state = game.state_string()
        if self.cutoff_test(state, depth):
            return self.eval_fn(game, self.identity)
        v = -math.inf
        for (a, s) in self.successors(state):
            v = max(v, self.min(s, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min(self, game, alpha, beta, depth):
        state = game.state_string()
        if self.cutoff_test(state, depth):
            return self.eval_fn(state, se)
        v = math.inf
        for (a, s) in self.successors(state):
            v = min(v, self.max(s, alpha, beta, depth+1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def valid_moves(self, game, piece_type):
        possible_placements = []
        for i in range(game.size):
            for j in range(game.size):
                if game.valid_place_check(i, j, piece_type, test_check=True):
                    possible_placements.append((i, j))
        possible_placements.append("PASS")
        return possible_placements

    def get_input(self, game):
        best_moves = []
        best_score = None
        best_black = MIN_SCORE
        best_white = MIN_SCORE
        for possible_move in self.valid_moves(game, self.identity):
            # Calculate the game state if we select this move.
            next_state = game.next_board(possible_move, self.identity)

            opponent_best_outcome = alpha_beta_result(
                next_state, self.max_depth,
                best_black, best_white,
                self.eval_fn)
            our_best_outcome = -1 * opponent_best_outcome
            if (not best_moves) or our_best_outcome > best_score:
                best_moves = [possible_move]
                best_score = our_best_outcome
                if game_state.next_player == Player.black:
                    best_black = best_score
                elif game_state.next_player == Player.white:
                    best_white = best_score
            elif our_best_outcome == best_score:
                best_moves.append(possible_move)
        return random.choice(best_moves)


def alpha_beta_result(next_state, max_depth, best_black, best_white, eval_fn):
    if game_state.is_over():  # <1>
        if game_state.winner() == game_state.next_player:  # <1>
            return MAX_SCORE  # <1>
        else:  # <1>
            return MIN_SCORE  # <1>

    if max_depth == 0:  # <2>
        return eval_fn(game_state)  # <2>

    best_so_far = MIN_SCORE
    for candidate_move in game_state.legal_moves():  # <3>
        next_state = game_state.apply_move(candidate_move)  # <4>
        opponent_best_result = alpha_beta_result(  # <5>
            next_state, max_depth - 1,  # <5>
            best_black, best_white,  # <5>
            eval_fn)  # <5>
        our_result = -1 * opponent_best_result  # <6>

        if our_result > best_so_far:  # <7>
            best_so_far = our_result  # <7>
        # end::alpha-beta-prune-1[]

        # tag::alpha-beta-prune-2[]
        if game_state.next_player == Player.white:
            if best_so_far > best_white:  # <8>
                best_white = best_so_far  # <8>
            outcome_for_black = -1 * best_so_far  # <9>
            if outcome_for_black < best_black:  # <9>
                return best_so_far  # <9>
        # end::alpha-beta-prune-2[]
        # tag::alpha-beta-prune-3[]
        elif game_state.next_player == Player.black:
            if best_so_far > best_black:  # <10>
                best_black = best_so_far  # <10>
            outcome_for_white = -1 * best_so_far  # <11>
            if outcome_for_white < best_white:  # <11>
                return best_so_far

    return best_so_far
