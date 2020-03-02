import pickle
import random

file = "qvalues_Anton_500000.pkl"
with open(file, 'rb') as pickle_file:
    qvals_dict = pickle.load(pickle_file)

state = []
action = []
q_value = []
for i in range(10):
    state.append(random.choice(list(qvals_dict)))
    actions = qvals_dict[state[i]]
    action.append(random.choice(list(actions)))
    q_value.append(actions[action])

# state = random.choice(list(qvals_dict))
# state.append(random.choice(list(qvals_dict)))
# actions = qvals_dict[state]
# action = random.choice(list(actions))
# q_value = actions[action]

file = "qvalues_Anton_1300000.pkl"
with open(file, 'rb') as pickle_file:
    qvals_dict = pickle.load(pickle_file)

q_value_newer = []
for i in range(10):
    q_value_newer.append(qvals_dict[state[i]][action[i]])

for old, new in q_value, q_value_newer:
    print('-'*90)
    print("  q_value_old = {}".format(old))
    print("q_value_newer = {}".format(new))
    print('-'*90)


#
# with open("TrackIntP1 Server.txt", "r") as file:
#     x = file.readlines()
#     rows = []
#     wins = []
#     losses = []
#     for y in x:
#         for w in y:
#             w = w.replace(',', '')
#             w = w.replace('[', '')
#             w = w.replace(']', '')


        # rows.append(i for i in y if i.isnumeric())
        # print(y)
