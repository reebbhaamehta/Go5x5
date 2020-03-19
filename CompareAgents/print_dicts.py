import copy
import pickle
import json


def stringify_keys(d):
    """Convert a dict's keys to strings if they are not."""
    di = copy.deepcopy(d)
    for key in di.keys():
        # check inner dict
        if isinstance(d[key], dict):
            value = stringify_keys(d[key])
        else:
            value = d[key]

        # convert nonstring to string if needed
        if not isinstance(key, str):
            try:
                d[str(key)] = value
            except Exception:
                try:
                    d[repr(key)] = value
                except Exception:
                    raise

            # delete old key
            del d[key]
    return d


if __name__ == "__main__":
    # if self.identity == 1:
    num_games = 20
    state_q_X = pickle.load(open("qvalues_X_{}.pkl".format(num_games), "rb"))
    state_q_O = pickle.load(open("qvalues_O_{}.pkl".format(num_games), "rb"))

    state_q_O = stringify_keys(state_q_O)
    state_q_X = stringify_keys(state_q_X)
    print(len(state_q_X))
    print(len(state_q_O))

    with open("X_dict.json", "w") as file:
        file.write(json.dumps(state_q_X, sort_keys=True, indent=4))
    with open("O_dict.json", "w") as file:
        file.write(json.dumps(state_q_O, sort_keys=True, indent=4))

    policy_X = pickle.load(open("policy_learned_X_{}.pkl".format(num_games), "rb"))
    policy_O = pickle.load(open("policy_learned_O_{}.pkl".format(num_games), "rb"))

    policy_O = stringify_keys(policy_O)
    policy_X = stringify_keys(policy_X)
    print(len(policy_O))
    print(len(policy_X))
    with open("X_policy.json", "w") as file:
        file.write(json.dumps(policy_X, sort_keys=True, indent=4))
    with open("O_policy.json", "w") as file:
        file.write(json.dumps(policy_O, sort_keys=True, indent=4))