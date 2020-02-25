from my_player3 import Q_learning_agent
from host import GO, judge
from read import readInput
from write import writeOutput
from random_player import RandomPlayer

BLACK = 1
WHITE = 2
LEARN_GAMES = 10

"""
Learning:
- play game of go through the host
- against random player & then itself
- select best moves based on q value tables
- update Q values after each game
- update table of q values for each state
"""


def play(go, player1, player2):
    player1.update_piece_type(BLACK)
    player2.update_piece_type(WHITE)
    n_move = 0
    while not go.game_end(player1.piece, action="MOVE"):
        n_move += 1
        player1.next_move(go, player1.piece)
        player2.next_move(go, player2.piece)
        go.judge(n_move)

    # board game is over now:
    if player1.__class__.__name__ == "Q_learning_agent":
        player1.update_Qvalues(go)
    if player2.__class__.__name__ == "Q_learning_agent":
        player2.update_Qvalues(go)

    return go.judge_winner()


if __name__ == "__main__":

    qlearner = Q_learning_agent(BLACK)
    random_player = RandomPlayer(WHITE)

    for i in range(LEARN_GAMES):
        go = GO(5)
        go.play(qlearner, random_player, True)

