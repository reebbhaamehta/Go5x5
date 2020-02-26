import sys

from my_player3 import Q_learning_agent
from host import GO, judge
from read import readInput, readOutput
from write import writeOutput, writeNextInput
from random_player import RandomPlayer

BLACK = 1
WHITE = 2
LEARN_GAMES = 1

"""
Learning:
- play game of go through the host
- against random player & then itself
- select best moves based on q value tables
- update Q values after each game
- update table of q values for each state
"""


def judget(n_move, go, verbose=False):
    N = 5

    piece_type, previous_board, board = readInput(N)
    go.verbose = verbose
    go.set_board(piece_type, previous_board, board)
    go.n_move = n_move
    try:
        action, x, y = readOutput()
    except:
        print("output.txt not found or invalid format")
        # sys.exit(3 - piece_type)
        return 3 - piece_type

    if action == "MOVE":
        if not go.place_chess(x, y, piece_type):
            print('Game end.')
            print('The winner is {}'.format('X' if 3 - piece_type == 1 else 'O'))
            # sys.exit(3 - piece_type)
            return 3 - piece_type

        go.died_pieces = go.remove_died_pieces(3 - piece_type)

    if verbose:
        go.visualize_board()
        print()

    if go.game_end(piece_type, action):
        result = go.judge_winner()
        if verbose:
            print('Game end.')
            if result == 3:
                print('The game is a tie.')
            else:
                print('The winner is {}'.format('X' if result == 1 else 'O'))
        # sys.exit(result)
        return result

    piece_type = 2 if piece_type == 1 else 1

    if action == "PASS":
        go.previous_board = go.board
    writeNextInput(piece_type, go.previous_board, go.board)
    return
    # sys.exit(0)


def play1(go, player1, player2):
    player1.update_piece_type(BLACK)
    player2.update_piece_type(WHITE)
    n_move = 0
    while True:
        n_move += 1
        action = player1.get_input(go, player1.piece)
        writeOutput(action)
        reward1 = judget(n_move, go, True)
        if reward1 == 1 or reward1 == 0 or reward1 == 2 or reward1 == -1 or reward1 == -2:
            break
        n_move += 1
        action = player2.get_input(go, player2.piece)
        writeOutput(action)
        reward2 = judget(n_move, go, True)
        if reward2 == 1 or reward2 == 0 or reward2 == 2 or reward2 == -1 or reward2 == -2:
            break

    # board game is over now:
    if player1.__class__.__name__ == "Q_learning_agent":
        player1.update_Qvalues(go, reward1)
    if player2.__class__.__name__ == "Q_learning_agent":
        player2.update_Qvalues(go, reward2)

    return go.judge_winner()


if __name__ == "__main__":

    qlearner = Q_learning_agent(BLACK)
    random_player = RandomPlayer(WHITE)

    for i in range(LEARN_GAMES):
        go = GO(5)
        go.init_board(5)
        # print(go.play(qlearner, random_player, True))
        go.play(qlearner, random_player, True)
        qlearner.update_Qvalues(go)

