# Python bytecode 3.6 (3379)
# Embedded file name: /Users/bo/Documents/projects/561/TA Spring 2020/QL-Example-For-TicTacToe/RandomPlayer.py
# Compiled at: 2020-01-31 08:30:12
# Size of source mod 2**32: 661 bytes
# Decompiled by https://python-decompiler.com
from Board import Board
import numpy as np


class RandomPlayer:

    def __init__(self, side=None):
        self.side = side

    def set_side(self, side):
        self.side = side

    def set_win_rates(self, wins):
        pass

    def move(self, board):
        if board.game_over():
            return
        else:
            candidates = []
            for i in range(0, 3):
                for j in range(0, 3):
                    if board.state[i][j] == 0:
                        candidates.append(tuple([i, j]))

            idx = np.random.randint(len(candidates))
            random_move = candidates[idx]
            return board.move(random_move[0], random_move[1], self.side)

    def learn(self, board):
        pass
