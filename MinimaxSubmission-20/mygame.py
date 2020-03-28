import copy

import numpy


# TODO:Rewrite entire class
class Game:

    def __init__(self, size):
        self.n_move = 0
        self.died_pieces = []
        self.verbose = None
        self.num_moves = 0
        self.max_move = size * size - 1  # The max movement of a Go game
        self.komi = size / 2  # Komi rule
        self.size = size
        self.board = numpy.array(numpy.zeros((self.size, self.size)))
        self.previous_board = copy.deepcopy(self.board)
        self.X_move = True
        self.next_board = copy.deepcopy(self.board)
        self.prev_opponent_score = 0
        self.opponent_score = 0
        self.opponent_prev_liberties = 0
        self.opponent_liberties = 0




    def next_board(self, possible_move, piece_type):
        board = self.board
        if possible_move != "PASS":
            board[possible_move[0]][possible_move[1]] = piece_type
        self.next_board = board
        return self.next_board

    def new_board(self):
        self.board = numpy.array([[0 for x in range(self.size)] for y in range(self.size)])  # Empty space marked as 0
        self.previous_board = copy.deepcopy(self.board)

    def state_string(self, state_type="Current"):
        """ Encode the current state of the board as a string
        """
        if state_type == "Current":
            state_string = str(self.board.ravel())[1:-1].strip()
            # return ''.join([str(self.board[i][j]) for i in range(self.size) for j in range(self.size)])
        elif state_type == "Previous":
            state_string = str(self.previous_board.ravel())[1:-1].strip()
        return state_string
        # return ''.join([str(self.previous_board[i][j]) for i in range(self.size) for j in range(self.size)])

    def game_end(self, action="MOVE"):
        """
        Check if the game should end.

        :param action: "MOVE" or "PASS".
        :return: boolean indicating whether the game should end.
        """

        # Case 1: max move reached
        if self.n_move >= self.max_move:
            return True
        # Case 2: two players all pass the move.
        if self.compare_board(self.previous_board, self.board) and action == "PASS":
            return True
        return False

    def score(self, piece_type):
        """
        Get score of a player by counting the number of stones.

        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the game should end.
        """

        board = self.board
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == piece_type:
                    count += 1
        return count

    def total_score(self, piece_type):
        """
        Get score of a player by counting the number of stones.

        :param piece_type: 1('X') or 2('O').
        :return: boolean indicating whether the game should end.
        """
        board = self.board
        count = 0
        count_opponent = 0
        if piece_type == 1:
            opponent = 2
        else:
            opponent = 1
        for i in range(self.size):
            for j in range(self.size):
                # if I place my piece in the center I get + 2 points
                if board[2][2] == piece_type:
                    count = count + 3
                # if I place a piece on the edges I get - 2 points
                if board[i][4] == piece_type or board[0][j] == piece_type:
                    count = count - 2
                # I get 1 point for each of my stones on the board
                if board[i][j] == piece_type:
                    count += 1
                    ally_members = self.ally_dfs(i, j)
                    for member in ally_members:
                        neighbors = self.detect_neighbor(member[0], member[1])
                        for piece in neighbors:
                        # If there is empty space around a piece, it has liberty
                            # I get + 2 points for each liberty I have
                            if board[piece[0]][piece[1]] == 0:
                                count += 2
                            # I get + 2 points if I place my stone near an opponents
                            if board[piece[0]][piece[1]] == opponent:
                                count += 2
                # if board[i][j] == opponent:
                    #count_opponent += 1
                    #ally_members = self.ally_dfs(i, j)
                    #for member in ally_members:
                        #neighbors = self.detect_neighbor(member[0], member[1])
                        #for piece in neighbors:
                            #if board[piece[0]][piece[1]] == 0:
                                #count_opponent += 1

        # I should get points if I minimize my opponents liberties.
        self.opponent_prev_liberties = self.opponent_liberties
        self.opponent_liberties = count_opponent
        if self.opponent_liberties < self.opponent_prev_liberties:
            count += 2

        # self.prev_opponent_score = self.opponent_score
        if piece_type == 1:
            count = count - self.komi
        #     self.opponent_score = self.score(2)
        # else:
        #     self.opponent_score = self.score(1)
        # if self.opponent_score < self.prev_opponent_score:
        #     count = count + 2
        return count

    def count_liberties(self, opponent):
        board = self.board
        count = 0
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] != opponent:
                    ally_members = self.ally_dfs(i, j)
                    for member in ally_members:
                        neighbors = self.detect_neighbor(member[0], member[1])
                        for piece in neighbors:
                            # If there is empty space around a piece, it has liberty
                            if board[piece[0]][piece[1]] == 0:
                                count += 1
        return count

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
            if verbose:
                print(('Invalid placement. row should be in the range 1 to {}.').format(len(board) - 1))
            return False
        if not (j >= 0 and j < len(board)):
            if verbose:
                print(('Invalid placement. column should be in the range 1 to {}.').format(len(board) - 1))
            return False

        # Check if the place already has a piece
        if board[i][j] != 0:
            if verbose:
                print('Invalid placement. There is already a chess in this position.')
            return False

        # Copy the board for testing
        test_go = copy.deepcopy(self)
        test_board = test_go.board

        # Check if the place has liberty
        test_board[i][j] = piece_type
        test_go.board = test_board
        if test_go.has_liberty(i, j):
            return True

        # If not, remove the died pieces of opponent and check again
        test_go.clean_dead_stones(3 - piece_type)
        if not test_go.has_liberty(i, j):
            if verbose:
                print('Invalid placement. No liberty found in this position.')
            return False

        # Check special case: repeat placement causing the repeat board state (KO rule)
        else:
            if self.died_pieces and self.compare_board(self.previous_board, test_go.board):
                if verbose:
                    print('Invalid placement. A repeat move not permitted by the KO rule.')
                return False
        return True

    def compare_board(self, board1, board2):
        for i in range(self.size):
            for j in range(self.size):
                if board1[i][j] != board2[i][j]:
                    return False
        return True

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
                if board[i][j] == piece_type:
                    # The piece die if it has no liberty
                    if not self.find_liberty(i, j):
                        died_pieces.append((i, j))
        return died_pieces

    def remove_certain_pieces(self, positions):
        """
        Remove the stones of certain locations.

        :param positions: a list containing the pieces to be removed row and column(row, column)
        :return: None.
        """
        board = self.board
        for piece in positions:
            board[piece[0]][piece[1]] = 0
        self.board = board

    def remove_died_pieces(self, piece_type):
        """
        Remove the dead stones in the board.

        :param piece_type: 1('X') or 2('O').
        :return: locations of dead pieces.
        """

        died_pieces = self.find_died_pieces(piece_type)
        if not died_pieces: return []
        self.remove_certain_pieces(died_pieces)
        return died_pieces

    def detect_neighbor(self, i, j):
        """
        Detect all the neighbors of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbors row and column (row, column) of position (i, j).
        """
        board = self.board
        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0: neighbors.append((i - 1, j))
        if i < len(board) - 1: neighbors.append((i + 1, j))
        if j > 0: neighbors.append((i, j - 1))
        if j < len(board) - 1: neighbors.append((i, j + 1))
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
        # Iterate through neighbors
        for piece in neighbors:
            # Add to allies list if having the same color
            if board[piece[0]][piece[1]] == board[i][j]:
                group_allies.append(piece)
        return group_allies

    def ally_dfs(self, i, j):
        """
        Using DFS to search for all allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the all allies row and column (row, column) of position (i, j).
        """
        stack = [(i, j)]  # stack for DFS serach
        ally_members = []  # record allies positions during the search
        while stack:
            piece = stack.pop()
            ally_members.append(piece)
            neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members

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

    def place_chess(self, i, j, piece_type, test_check):
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
        self.previous_board = copy.deepcopy(board)
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
            if piece_type == 1:
                action = player1.get_input(self, piece_type)
            else:
                action = player2.get_input(self, piece_type)

            # print(action)
            if verbose:
                player = "X" if piece_type == 1 else "O"

            if action != "PASS":
                # If invalid input, continue the loop. Else it places a chess on the board.
                if not self.place_chess(action[0], action[1], piece_type, True):

                    if piece_type == 1:
                        print("-"*60)
                        print("X turn: player1")
                        print(self.previous_board)
                        print(action)
                        print(self.board)
                        print("-"*60)
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
                self.previous_board = copy.deepcopy(self.board)

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
            # index=0
            # for line in lines[1:self.size + 1]:
            #     line = line.rstrip("\n")
            #     previous_board.append([])
            #     for letter in line:
            #         previous_board[index].append(int(letter))
            #     index +=1
            self.board = [[int(x) for x in line.rstrip('\n')] for line in lines[self.size + 1: 2 * self.size + 1]]
            # self.board = []
            # index=0
            # for line in lines[self.size + 1:2 * self.size + 1]:
            #     line = line.rstrip("\n")
            #     self.board.append([])
            #     for letter in line:
            #         self.board[index].append(int(letter))
            #     index +=1
            return self.piece_type, self.previous_board, self.board

    def write_output(self, result):
        res = self.piece_type
        with open("output.txt", 'w') as f:
            if result == "PASS":
                f.write(result)
            else:
                f.write(str(result[0]) + ',' + str(result[1]))
