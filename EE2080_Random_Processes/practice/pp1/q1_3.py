import numpy as np
import matplotlib.pyplot as plt

M = 10000
N = 3
size = 10
tol = 0.2

def Y_path():
    X = np.random.standard_normal(size)
    Y = np.array([])

    for n in range(size):
        y = 0

        for i in range(N - 1):
            if n - i >= 0:
                y += X[n - i]
            else:
                break

        Y = np.append(Y, y/N)

    return Y

paths_Y = np.array([Y_path() for _ in range(M)])

mean_path_Y = np.array([np.mean(paths_Y[:, n]) for n in range(size)])
plt.plot(range(size), mean_path_Y)
plt.show()

cov_path_Y = np.zeros((size, size))

for n1 in range(size):
    for n2 in range(size):
        cov = 0
        for i in range(M):
            cov += paths_Y[i][n1] * paths_Y[i][n2]

        cov_path_Y[n1][n2] = cov/M 

wss = 1
predicted_mean = mean_path_Y[0]

for n in range(size):
    max_tolerable_mean = tol if predicted_mean == 0 else predicted_mean*(1 + tol)
    min_tolerable_mean = -tol if predicted_mean == 0 else predicted_mean*(1 - tol)

    if ((predicted_mean > 0 and not min_tolerable_mean <= mean_path_Y[n] <= max_tolerable_mean)
        or (predicted_mean <= 0 and not max_tolerable_mean <= mean_path_Y[n] <= min_tolerable_mean)):

        wss = 0 
        print("Y is NOT WSS")
        break


for n1 in range(size):
    for n2 in range(size):
        for h in range(min([size - n1, size - n2])):
            if cov_path_Y[n1][n2] != cov_path_Y[n1 + h][n2 + h] and wss:
                print("Y is NOT WSS")
                wss = 0
                break
        if not wss: break
    if not wss: break

if(wss):
    print("Y is WSS")
