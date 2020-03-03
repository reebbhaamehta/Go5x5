import argparse
import pickle
import random
from my_player3 import Q_learning_agent


def read_qvals(file_old, file_new):
    file = "qvalues_Anton_500000.pkl"
    with open(file_old, 'rb') as pickle_file:
        qvals_dict = pickle.load(pickle_file)

    state = []
    action = []
    q_value = []
    for i in range(10):
        state.append(random.choice(list(qvals_dict)))
        actions = qvals_dict[state[i]]
        action.append(random.choice(list(actions)))
        q_value.append(actions[action[i]])

    file = "qvalues_Anton_1300000.pkl"
    with open(file_new, 'rb') as pickle_file:
        qvals_dict = pickle.load(pickle_file)

    q_value_newer = []
    for i in range(10):
        q_value_newer.append(qvals_dict[state[i]][action[i]])

    # print(q_value_newer)
    # print(q_value)
    for old, new in zip(q_value, q_value_newer):
        print('-' * 60)
        print("  q_value_old = {}".format(old))
        print("q_value_newer = {}".format(new))
        print('-' * 60)

    # state = random.choice(list(qvals_dict))
    # state.append(random.choice(list(qvals_dict)))
    # actions = qvals_dict[state]
    # action = random.choice(list(actions))
    # q_value = actions[action]


def policies(file_old, file_new):
    file_old = "policy_learned_0E_1583192958.pkl"
    with open(file_old, 'rb') as pickle_file:
        policy_dict = pickle.load(pickle_file)
    states = []
    policy = []
    for i in range(10):
        states.append(random.choice(list(policy_dict)))
        policy.append(policy_dict[states[i]])

    file_new = "policy_learned_0E_1583194212.pkl"  #"policy_learned_0E_1583192958.pkl"
    with open(file_new, 'rb') as pickle_file:
        policy_dict = pickle.load(pickle_file)

    policy_newer = []
    for i in range(10):
        policy_newer.append(policy_dict[states[i]])

    # print(q_value_newer)
    # print(q_value)
    for old, new in zip(policy, policy_newer):
        print('-' * 60)
        print("  q_value_old = {}".format(old))
        print("q_value_newer = {}".format(new))
        print('-' * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_old", type=str, help="Initial qvalue file", default="")
    parser.add_argument("--file_new", type=str, help="Final qvalue file", default="")
    args = parser.parse_args()
    policies(args.file_old, args.file_new)
    # read_qvals(args.file_old, args.file_new)
