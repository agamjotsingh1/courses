import numpy as np
import matplotlib.pyplot as plt

MAX_ITER = int(1e+3)

k = 40
n = 60
p1 = 0.6
p2 = 0.4

def gen_X_path(k, n, p1, p2, T=10, policy="always_1"):
    X = np.array([k,])
    next_bt = 1

    for _ in range(MAX_ITER):
        bt = 0
        outcome = 0
        wealth = X[-1]

        if(policy == "always_1"):
            bt = 1
        elif(policy == "always_2"):
            bt = 2 if wealth >= 2 else 1
        elif(policy == "pessimistic"):
            bt = 1 if p1 >= p2 else 2
        elif(policy == "uniform_random"):
            bt = np.random.choice([1, 2])
        elif(policy == "threshold"):
            bt = 2 if wealth >= T else 1
        elif(policy == "adaptive"):
            bt = next_bt

        if bt == 1: outcome = bt if np.random.uniform(0, 1) < p1 else -bt
        elif bt == 2: outcome = bt if np.random.uniform(0, 1) < p2 else -bt

        if outcome == bt: next_bt = 2
        else: next_bt = 1

        if wealth + outcome >= n:
            X = np.append(X, n)
            return X

        elif wealth + outcome <= 0:
            X = np.append(X, 0)
            return X

        X = np.append(X, wealth + outcome)

    return X

def monte_carlo(num=10000, T=10, policy="always_1"):
        num_wins = 0
        stopping_times = np.array([])

        for _ in range(num):
            path_X = gen_X_path(k, n, p1, p2, T, policy=policy)

            if path_X[-1] == n:
                num_wins += 1

            stopping_times = np.append(stopping_times, len(path_X))

        success_prob = num_wins/num
        print(num_wins, num, success_prob)

        return success_prob, stopping_times

table = {}

# for policy in ["always_1", "always_2", "pessimistic", "uniform_random", "threshold", "adaptive"]:
for policy in ["threshold"]:
    for _ in range(2):
        path_X = gen_X_path(k, n, p1, p2, T=10, policy=policy)
        plt.plot(range(len(path_X)), path_X, label=f"X_n Path #{k}, Policy={policy}")

    plt.legend(loc="best")
    plt.show()

    success_prob, stopping_times = monte_carlo(T=10, policy=policy)
    avg_stopping_time = np.mean(stopping_times)

    table[policy] = [success_prob, avg_stopping_time]

    plt.hist(stopping_times, label="Stopping times Histogram")

    plt.legend()
    plt.show()

    success_probs = np.array([])
    avg_stopping_times = np.array([])
    T_range = range(2, 22, 2)

    for T in T_range:
        success_prob, stopping_times = monte_carlo(T=T, policy=policy)
        success_probs = np.append(success_probs, success_prob)
        avg_stopping_times = np.append(avg_stopping_times, np.mean(stopping_times))

    print(avg_stopping_times)

    plt.stem(T_range, success_probs, label = "Success Probability")
    plt.legend()
    plt.show()

    plt.stem(T_range, avg_stopping_times, label = "Avg Stopping Times")
    plt.legend()
    plt.show()

print(table)
