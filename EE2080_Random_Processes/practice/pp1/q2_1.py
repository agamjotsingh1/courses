import numpy as np
import matplotlib.pyplot as plt

MAX_ITER = int(1e+6)

k = 40
n = 60
p = 0.5

def gen_X_path(k, n, p):
    X = np.array([k,])

    for i in range(1, MAX_ITER):
        outcome = 1 if np.random.uniform(0, 1) < p else -1
        if X[i - 1] + outcome >= n or X[i - 1] + outcome <= 0:
            X = np.append(X, X[i - 1] + outcome)
            return X

        X = np.append(X, X[i - 1] + outcome)

    return X


for _ in range(5):
    path_X = gen_X_path(k, n, p)
    plt.plot(range(len(path_X)), path_X, label=f"X_n Path #{k}")

plt.legend(loc="best")
plt.show()


def monte_carlo(num=10000):
    results = np.array([])
    win_stopping_times = np.array([])
    lose_stopping_times = np.array([])

    for _ in range(num):
        path_X = gen_X_path(k, n, p)

        if path_X[-1] == n:
            if len(win_stopping_times) <= 100: win_stopping_times = np.append(win_stopping_times, len(path_X))
            results = np.append(results, 1)
        elif path_X[-1] == 0:
            if len(lose_stopping_times) <= 100: lose_stopping_times = np.append(lose_stopping_times, len(path_X))
            results = np.append(results, 0)

    return np.mean(results), win_stopping_times, lose_stopping_times

results, win_stopping_times, lose_stopping_times = monte_carlo()

plt.plot(range(len(win_stopping_times)), win_stopping_times, label="Winning stopping times")
plt.plot(range(len(lose_stopping_times)), lose_stopping_times, label="Losing stopping times")
plt.legend()
plt.show()

print("Probability of Gambler winning in Monte Carlo = ", results)
