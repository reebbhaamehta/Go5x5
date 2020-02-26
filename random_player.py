import random
import sys
from read import readInput
from write import writeOutput

from host import GO


class RandomPlayer():
    def __init__(self, piece_type):
        self.type = 'random'
        self.piece = piece_type

    def get_input(self, go, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''
        possible_placements = []
        for i in range(go.size):
            for j in range(go.size):
                if go.valid_place_check(i, j, piece_type, test_check=False):
                    possible_placements.append((i, j))

        if not possible_placements:
            return "PASS"
        else:
            return random.choice(possible_placements)

    def update_piece_type(self, piece):
        self.piece = piece


if __name__ == "__main__":
    N = 5
    piece_type, previous_board, board = readInput(N)
    go = GO(N)
    go.set_board(piece_type, previous_board, board)
    player = RandomPlayer()
    action = player.get_input(go, piece_type)
    writeOutput(action)
