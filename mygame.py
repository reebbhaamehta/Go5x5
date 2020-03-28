from copy import copy
import numpy
import json
import time

class GameEncoder(json.JSONEncoder):
    def default(self, obj):
      if isinstance(obj, Game):
        return {
          "n_move": obj.n_move,
          "died_pieces": obj.died_pieces,
          "verbose": obj.verbose,
          "num_moves": obj.num_moves,
          "max_moves": obj.max_moves,
          "komi": obj.komi,
          "size": obj.size,
          "board": obj.board.tolist(),
          "previous_board": obj.previous_board.tolist(),
          "X_move": obj.X_move,
          "prev_opponent_score": obj.prev_opponent_score,
          "opponent_score": obj.opponent_score,
          "opponent_prev_liberties": obj.opponent_prev_liberties,
          "opponent_liberties": obj.opponent_liberties,
          "new_game": obj.new_game,
        }
      return super(GameEncoder, self).default(obj)


class GameDecoder(json.JSONDecoder):
  def __init__(self, *args, **kwargs):
    json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

  def object_hook(self, obj):
    # if isinstance(obj, Game):
    g = Game(5)
    g.__dict__.update(obj)
    g.board = numpy.array(g.board)
    g.previous_board = numpy.array(g.previous_board)
    return g


class Game:
    def __init__(self, size):
        self.n_move = 0
        self.died_pieces = []
        self.verbose = None
        self.num_moves = 0
        self.max_moves = size * size - 1  # The max movement of a Go game
        self.komi = size / 2.  # Komi rule
        self.size = size
        self.board = numpy.array(numpy.zeros((self.size, self.size)))
        self.previous_board = numpy.array(self.board)
        self.X_move = True
        self.prev_opponent_score = 0
        self.opponent_score = 0
        self.opponent_prev_liberties = 0
        self.opponent_liberties = 0
        self.new_game = False

    def next_board(self, i, j, piece_type, test_check=True):
        # Saves the board after placing the stone and removing died pieces.
        valid_placement = self.place_new_stone(i, j, piece_type, test_check)
        if not valid_placement:
            raise ValueError("in next_board, invalid move")
        # Remove the dead pieces of opponent
        self.died_pieces = self.clean_dead_stones(3 - piece_type)
        self.remove_stones(self.died_pieces)
        return valid_placement

    def new_board(self):
        self.board = numpy.zeros((self.size, self.size)) # Empty space marked as 0
        self.previous_board = numpy.array(self.board)

    def state_string(self, state_type="Current"):
        """
        Encode the current state of the board as a string
        """
        tmp = None
        if state_type == "Current":
            tmp = self.board.ravel()
        elif state_type == "Previous":
            tmp = self.previous_board.ravel()
        return " ".join(map(str, tmp))

    def is_game_finished(self, action="MOVE"):
        # Case 1: max moves
        if self.n_move >= self.max_moves:
            return True
        # Case 2: both players pass.
        if self.compare_board(self.previous_board, self.board) and action == "PASS":
            return True
        return False

    def count_player_stones(self, piece_type):
        board = self.board
        return numpy.count_nonzero(board == piece_type)

    def has_liberty(self, i, j):
        board = self.board
        island = self.ally_dfs(i, j)
        for position in island:
            adjacent_stones = self.gimme_adjacent(position[0], position[1])
            for stone in adjacent_stones:
                if board[stone[0]][stone[1]] == 0:
                    return True
        return False

    def island_with_liberty(self, i, j):
        board = self.board
        island = self.ally_dfs(i, j)
        for position in island:
            adjacent_stones = self.gimme_adjacent(position[0], position[1])
            for stone in adjacent_stones:
                if board[stone[0]][stone[1]] == 0:
                    return None
        return island

    def is_position_valid(self, i, j, piece_type, *args, **kwargs):
        board = self.board
        if not (i >= 0 and i < len(board)):
            return False
        if not (j >= 0 and j < len(board)):
            return False

        if board[i][j] != 0:
            return False

        test_go = self.make_copy()
        test_board = test_go.board

        test_board[i][j] = piece_type
        test_go.board = test_board
        if test_go.has_liberty(i, j):
            return True

        test_go.clean_dead_stones(3 - piece_type)
        if not test_go.has_liberty(i, j):
            return False
        else:
            if self.died_pieces and numpy.array_equal(self.previous_board, test_go.board):
                return False
        return True

    def compare_board(self, board1, board2):
        return numpy.array_equal(board1, board2)

    def make_copy(self):
        g = Game(self.size)
        g.n_move = copy(self.n_move)
        g.died_pieces = self.died_pieces.copy()
        g.verbose = copy(self.verbose)
        g.num_moves = copy(self.num_moves)
        g.max_moves = copy(self.max_moves)
        g.komi = copy(self.komi)
        g.size = copy(self.size)
        g.board = numpy.array(self.board, dtype='int')
        g.previous_board = numpy.array(self.previous_board, dtype='int')
        g.X_move = copy(self.X_move)
        g.prev_opponent_score = copy(self.prev_opponent_score)
        g.opponent_score = copy(self.opponent_score)
        g.opponent_prev_liberties = copy(self.opponent_prev_liberties)
        g.opponent_liberties = copy(self.opponent_liberties)
        g.new_game = copy(self.new_game)
        return g

    def find_dead_stones(self, stone_type):
        board = self.board
        kills = []
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == stone_type and (i, j) not in kills:
                    tmp = self.island_with_liberty(i, j)
                    if tmp is not None:
                        kills += tmp
        return kills

    def remove_stones(self, positions):
        board = self.board
        for x, y in positions:
            board[x][y] = 0
        self.board = board

    def clean_dead_stones(self, stone_type):
        dead_stones = self.find_dead_stones(stone_type)
        if not dead_stones:
            return []
        self.remove_stones(dead_stones)
        return dead_stones

    def gimme_adjacent(self, i, j):
        adjacent_stones = []
        if i > 0: adjacent_stones.append((i - 1, j))
        if i < self.size - 1: adjacent_stones.append((i + 1, j))
        if j > 0: adjacent_stones.append((i, j - 1))
        if j < self.size - 1: adjacent_stones.append((i, j + 1))
        return adjacent_stones

    def detect_adj_my_island(self, i, j):
        board = self.board
        adjacent_stones = self.gimme_adjacent(i, j)  # Detect neighbors
        island_memebers = []
        piece = board[i][j]
        for p_i, p_j in adjacent_stones:
            if board[p_i][p_j] == piece:
                island_memebers.append((p_i, p_j))
        return island_memebers

    def ally_dfs(self, i, j):
        to_be_checked = [(i, j)]
        island_members = []
        while to_be_checked:
            stone = to_be_checked.pop()
            island_members.append(stone)
            adjacent_stones = self.detect_adj_my_island(stone[0], stone[1])
            for island_mate in adjacent_stones:
                if island_mate not in to_be_checked and island_mate not in island_members:
                    to_be_checked.append(island_mate)
        return sorted(island_members)

    def set_board(self, stone_type, previous_board, board):
        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == stone_type and board[i][j] != stone_type:
                    self.died_pieces.append((i, j))
        self.previous_board = previous_board
        self.board = board

    def place_new_stone(self, i, j, piece_type, test_check):
        board = self.board
        if not self.is_position_valid(i, j, piece_type, test_check):
            return False
        self.previous_board = numpy.array(board)
        board[i][j] = piece_type
        self.board = numpy.array(board)
        return True

    def and_the_winner_is___(self):
        scores = self.game_scores()
        if scores[0] > scores[1]:
            return 1
        elif scores[0] < scores[1]:
            return 2
        else:
            return 0

    def game_scores(self):
        cnt_1 = self.count_player_stones(1)
        cnt_2 = self.count_player_stones(2)
        return cnt_1, cnt_2 + self.komi

    def visualize_board(self):
        board = self.board

        print('-' * len(board) * 2)
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    print(' ', end=' ')
                elif board[i][j] == 1:
                    print('X', end=' ')
                else:
                    print('O', end=' ')
            print()
        print('-' * len(board) * 2)

    def play(self, player1, player2, verbose=False):
        """
        The game starts!

        :param player1: Player instance. always X
        :param player2: Player instance. always O
        :param verbose: whether print input hint and error information
        :return: piece type of winner of the game (0 if it's a tie).
        """
        self.new_board()
        verbose = self.verbose
        # Game starts!
        while 1:
            piece_type = 1 if self.X_move else 2

            # Judge if the game should end
            if self.is_game_finished(piece_type):
                result = self.and_the_winner_is___()
                if verbose:
                    print('Game ended.')
                    if result == 0:
                        print('The game is a tie.')
                    else:
                        print('The winner is {}'.format('X' if result == 1 else 'O'))
                return result

            if verbose:
                player = "X" if piece_type == 1 else "O"
                print(player + " makes move...")

            # Game continues
            st = time.time()
            if piece_type == 1:
                action = player1.get_input(self, piece_type)
            else:
                action = player2.get_input(self, piece_type)
            print("Player {} took {} to make a move".format(piece_type, time.time()-st))
            # print(action)
            if verbose:
                player = "X" if piece_type == 1 else "O"

            if action != "PASS":
                # If invalid input, continue the loop. Else it places a chess on the board.
                if not self.place_new_stone(action[0], action[1], piece_type, True):

                    if piece_type == 1:
                        print("-" * 60)
                        print("X turn: player1")
                        print(self.previous_board)
                        print(action)
                        print(self.board)
                        print("-" * 60)
                        exit()
                    elif piece_type == 2:
                        print("O turn: player2")
                        print(action)
                        self.visualize_board()
                        print(self.previous_board)
                    if verbose:
                        self.visualize_board()
                    # continue
                    return -1  # return -1 if the move is invalid for training purposes

                self.died_pieces = self.clean_dead_stones(3 - piece_type)  # Remove the dead pieces of opponent
            else:
                self.previous_board = numpy.array(self.board)

            if verbose:
                self.visualize_board()  # Visualize the board again
                print()

            self.n_move += 1
            self.X_move = not self.X_move  # Players take turn

    def read_input(self):
        with open("input.txt", 'r') as f:
            lines = f.readlines()
            self.piece_type = int(lines[0])  # piece type being assigned to self is probably incorrect. Review.
            self.previous_board = [[int(letter) for letter in line.rstrip("\n")] for line in lines[1:self.size + 1]]

            self.board = [[int(x) for x in line.rstrip('\n')] for line in lines[self.size + 1: 2 * self.size + 1]]

        with open("helper.txt", "r") as f:
            test = f.readline().strip()
            self.n_move = int(test)

        if not numpy.any(self.board) and self.piece_type == 1:
            self.new_game = True
            self.n_move = 0
        elif numpy.sum(self.board) < 2 and self.piece_type == 2:
            self.new_game = True
            self.n_move = 1

        return self.piece_type, self.previous_board, self.board, self.n_move

    def write_output(self, result):
        with open("helper.txt", "w") as f:
            f.write(str(self.n_move))
        with open("output.txt", 'w') as f:
            if result == "PASS":
                f.write(result)
            else:
                f.write(str(result[0]) + ',' + str(result[1]))
