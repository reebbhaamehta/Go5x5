from my_player3 import Q_learning_agent

if __name__ == "__main__":
    q_learner = Q_learning_agent()
    q_learner.load_dict(0)
    q_learner.save_policy(0)
