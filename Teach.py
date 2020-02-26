import filecmp
import pickle
import sys

from my_player3 import Q_learning_agent
from host import GO, judge
from read import readInput, readOutput
from write import writeOutput, writeNextInput
from random_player import RandomPlayer

X = 1
O = 2
LEARN_GAMES = 1000

"""
Learning:
- play game of go through the host
- against random player & then itself
- select best moves based on q value tables
- update Q values after each game
- update table of q values for each state
"""


if __name__ == "__main__":

    qlearner = Q_learning_agent()

    random_player = RandomPlayer()
    random_player2 = RandomPlayer()



    for i in range(LEARN_GAMES):
        go = GO(5)
        go.init_board(5)
        go.play(random_player, qlearner, True)
        qlearner.update_Qvalues(go)

    file = "qlearner.txt"
    with open(file, 'w') as f:
        f.write(str(qlearner.q_values))
    qlearner_100games = Q_learning_agent()
    qlearner_100games.load_dict()
    file = "qlearner_100.txt"
    with open(file, 'w') as f:
        f.write(str(qlearner_100games.q_values))
    print(filecmp.cmp("qlearner.txt", "qlearner_100.txt"))
