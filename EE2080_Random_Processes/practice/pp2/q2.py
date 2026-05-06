import numpy as np
import matplotlib.pyplot as plt

# replacing [1, .., 6] indexing to [0, .., 5]
P = np.array([[0, 0.5, 0.5, 0, 0, 0],
              [0, 0, 0.5, 0.5, 0, 0],
              [0.5, 0, 0, 0, 0.5, 0],
              [0, 0.5, 0, 0, 0, 0.5],
              [0, 0, 0.5, 0, 0, 0.5],
              [0.5, 0, 0, 0.5, 0, 0]])

alpha = 0.85
tol = 1e-10
n = 6

J = np.ones((n, n))
G = (alpha*P) + ((1 - alpha)/n)*J
pi = np.ones(n)/n

MAX_K = 10000

for k in range(MAX_K):
    next_pi = pi @ G
    next_pi = next_pi / sum(next_pi)

    if np.linalg.norm(next_pi - pi) < tol:
        pi = next_pi
        break

    pi = next_pi

print("Stationary pi (iteratively) = ", pi)

eigenvals, eigenvecs = np.linalg.eig(G.T) 
stationary_pi = np.zeros(n)

for i in range(len(eigenvals)):
    if 1 - 1e-3 <= eigenvals[i] <= 1 + 1e-3:
        stationary_pi = eigenvecs[:, i]
        stationary_pi = stationary_pi/sum(stationary_pi)
        break

print("Stationary Pi (theoretical) = ", stationary_pi)
