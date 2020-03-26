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

# TODO:Rewrite entire class
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
        # saves the board after pacing the stone and removing died pieces.
        valid_placement = self.place_new_stone(i, j, piece_type, test_check)
        if not valid_placement:
            raise ValueError("in next_board, invalid move")
        # Remove the dead pieces of opponent
        self.died_pieces = self.remove_died_pieces(3 - piece_type)
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

    def game_end(self, action="MOVE"):
        # Case 1: max moves
        if self.n_move >= self.max_moves:
            return True
        # Case 2: both players pass.
        if self.compare_board(self.previous_board, self.board) and action == "PASS":
            return True
        return False

    def score(self, piece_type):
        board = self.board
        return numpy.count_nonzero(board == piece_type)

    def find_liberty(self, i, j):
        """
        Find liberty of a given stone. If a group of allied stones has no liberty, they all die.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: boolean indicating whether the given stone still has liberty.
        """
        board = self.board
        ally_members = self.ally_dfs(i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    return True
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return False

    def find_liberty_group(self, i, j):
        """
        Find liberty of a given stone. If a group of allied stones has no liberty, they all die.
        Returns all stones part of such group.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: boolean indicating whether the given stone still has liberty.
        """
        board = self.board
        ally_members = self.ally_dfs(i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    return None
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return ally_members

    def valid_place_check(self, i, j, piece_type, test_check=False):
        """
        Check whether a placement is valid.

        :param i: row number of the board.
        :param j: column number of the board.
        :param piece_type: 1(white piece)(X) or 2(black piece)(O).
        :param test_check: boolean if it's a test check.
        :return: boolean indicating whether the placement is valid.
        """
        board = self.board
        verbose = self.verbose
        if test_check:
            verbose = False
        # Check if the place is in the board range
        if not (i >= 0 and i < len(board)):
            return False
        if not (j >= 0 and j < len(board)):
            return False

        # Check if the place already has a piece
        if board[i][j] != 0:
            return False

        test_go = self.make_copy()
        test_board = test_go.board

        # Check if the place has liberty
        test_board[i][j] = piece_type
        test_go.board = test_board
        if test_go.find_liberty(i, j):
            return True

        # If not, remove the died pieces of opponent and check again
        test_go.remove_died_pieces(3 - piece_type)
        if not test_go.find_liberty(i, j):
            return False
        # Check for repeat placement
        else:
            if self.died_pieces and self.compare_board(self.previous_board, test_go.board):
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

    def find_died_pieces(self, piece_type):
        """
        Find the died stones that has no liberty in the board for a given piece type.

        :param piece_type: 1('X') or 2('O').
        :return: a list containing the dead pieces row and column(row, column).
        """
        board = self.board
        died_pieces = []
        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if board[i][j] == piece_type and (i,j) not in died_pieces:
                    # The piece die if it has no liberty
                    tmp = self.find_liberty_group(i,j)
                    if tmp is not None:
                        died_pieces += tmp
        return died_pieces

    def remove_stones(self, positions):
        board = self.board
        for x,y in positions:
            board[x][y] = 0
        self.board = board

    def remove_died_pieces(self, piece_type):
        """
        Remove the dead stones in the board.

        :param piece_type: 1('X') or 2('O').
        :return: locations of dead pieces.
        """

        died_pieces = self.find_died_pieces(piece_type)
        if not died_pieces:
            return []
        self.remove_stones(died_pieces)
        return died_pieces

    def detect_neighbor(self, i, j):
        """
        Detect all the neighbors of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbors row and column (row, column) of position (i, j).
        """
        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0: neighbors.append((i - 1, j))
        if i < self.size - 1: neighbors.append((i + 1, j))
        if j > 0: neighbors.append((i, j - 1))
        if j < self.size - 1: neighbors.append((i, j + 1))
        return neighbors

    def detect_neighbor_ally(self, i, j):
        """
        Detect the neighbor allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
        """
        board = self.board
        neighbors = self.detect_neighbor(i, j)  # Detect neighbors
        group_allies = []
        piece = board[i][j]
        # Iterate through neighbors
        for p_i, p_j in neighbors:
            # Add to allies list if having the same color
            if board[p_i][p_j] == piece:
                group_allies.append((p_i, p_j))
        return group_allies

    def ally_dfs(self, i, j):
        """
        Using DFS to search for all allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the all allies row and column (row, column) of position (i, j).
        """
        ini = (i, j)
        stack = [(i, j)]  # stack for DFS serach
        ally_members = []  # record allies positions during the search
        while stack:
            piece = stack.pop()
            ally_members.append(piece)
            neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return sorted(ally_members)

    def set_board(self, piece_type, previous_board, board):
        """
        Initialize board status.
        :param previous_board: previous board state.
        :param board: current board state.
        :return: None.
        """

        # 'X' pieces marked as 1
        # 'O' pieces marked as 2

        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == piece_type and board[i][j] != piece_type:
                    self.died_pieces.append((i, j))

        # self.piece_type = piece_type
        self.previous_board = previous_board
        self.board = board

    def place_new_stone(self, i, j, piece_type, test_check):
        """
        Place a chess stone in the board.

        :param i: row number of the board.
        :param j: column number of the board.
        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the placement is valid.
        """
        board = self.board
        valid_place = self.valid_place_check(i, j, piece_type, test_check)
        if not valid_place:
            return False
        self.previous_board = numpy.array(board)
        board[i][j] = piece_type
        self.board = numpy.array(board)
        return True

    def judge_winner(self):
        """
        Judge the winner of the game by number of pieces for each player.

        :param: None.
        :return: piece type of winner of the game (0 if it's a tie).
        """

        cnt_1 = self.score(1)
        cnt_2 = self.score(2)
        if cnt_1 > cnt_2 + self.komi:
            return 1
        elif cnt_1 < cnt_2 + self.komi:
            return 2
        else:
            return 0

    def komi_score(self):

        cnt_1 = self.score(1)
        cnt_2 = self.score(2)
        if cnt_1 > cnt_2 + self.komi:
            return cnt_1
        elif cnt_1 < cnt_2 + self.komi:
            return cnt_2
        else:
            return 0

    def visualize_board(self):
        '''
        Visualize the board.

        :return: None
        '''
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
            if self.game_end(piece_type):
                result = self.judge_winner()
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

                self.died_pieces = self.remove_died_pieces(3 - piece_type)  # Remove the dead pieces of opponent
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
