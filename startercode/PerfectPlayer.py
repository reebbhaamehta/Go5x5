# Python bytecode 3.6 (3379)
# Embedded file name: /Users/bo/Documents/projects/561/TA Spring 2020/QL-Example-For-TicTacToe/PerfectPlayer.py
# Compiled at: 2020-01-31 08:30:12
# Size of source mod 2**32: 2556 bytes
from Board import Board

WIN_REWARD = 1.0
DRAW_REWARD = 0.0
LOSS_REWARD = -1.0


class PerfectPlayer:

    def __init__(self, side=None):
        self.side = side
        self.transition = {}
        self.num_game = 0

    def set_side(self, side):
        self.side = side

    def set_win_rates(self, wins):
        pass

    def learn(self, board):
        pass

    def move(self, board: Board):
        if board.game_over():
            return
        else:
            score, action = self._max(board)
            return board.move(action[0], action[1], self.side)

    def _min(self, board):
        state = board.encode_state()
        if state in self.transition:
            return self.transition[state]
        elif board.game_result == 0:
            return (DRAW_REWARD, None)
        elif board.game_result == self.side:
            return (WIN_REWARD, None)
        elif board.game_result > 0:
            return (LOSS_REWARD, None)
        else:
            min_value, action = WIN_REWARD, None
            candidates = []
            for i in range(3):
                for j in range(3):
                    if board.state[i][j] == 0:
                        candidates.append((i, j))
            # candidates = [(i, j) for i in range(3) if board.state[i][j] == 0 for j in iter(range(3))]
            for i, j in candidates:
                copyBoard = Board(board.state)
                if self.side == 1:
                    opponent = 2
                else:
                    opponent = 1
                copyBoard.move(i, j, opponent)
                score, a = self._max(copyBoard)
                if score < min_value or action == None:
                    min_value, action = score, (i, j)
                    if min_value == LOSS_REWARD:
                        self.transition[state] = (
                            min_value, action)
                        break
                self.transition[state] = (
                    min_value, action)

            return (min_value, action)

    def _max(self, board):
        state = board.encode_state()
        if state in self.transition:
            return self.transition[state]
        elif board.game_result == 0:
            return (DRAW_REWARD, None)
        elif board.game_result == self.side:
            return (WIN_REWARD, None)
        elif board.game_result > 0:
            return (LOSS_REWARD, None)
        else:
            max_value, action = DRAW_REWARD, None
            candidates = []
            for i in range(3):
                for j in range(3):
                    if board.state[i][j] == 0:
                        candidates.append((i, j))
            # candidates = [(i, j) for i in range(3) if board.state[i][j] == 0 for j in iter(range(3))]
            for i, j in candidates:
                b = Board(board.state)
                b.move(i, j, self.side)
                score, a = self._min(b)
                if score > max_value or action == None:
                    max_value, action = score, (i, j)
                    if max_value == WIN_REWARD:
                        self.transition[state] = (
                            max_value, action)
                        break
                self.transition[state] = (
                    max_value, action)

            return (max_value, action)
