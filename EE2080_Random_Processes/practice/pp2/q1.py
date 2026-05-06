import numpy as np
import matplotlib.pyplot as plt

N = int(1e+3)

P = np.array([[0.7, 0.2, 0.1],
              [0.3, 0.4, 0.3],
              [0.2, 0.3, 0.5]])

pi = np.array([1, 0, 0])

# --- Q1.1 ---
#
# weather = np.array([])
#
# for n in range(365):
#     probs = pi @ P
#
#     # 0 for S, 1 for C, 2 for R
#     choice = np.random.choice(np.array([0, 1, 2]), p=list(probs))
#     weather = np.append(weather, choice)
#
#     # updating pi to current state
#     pi = np.zeros(3)
#     pi[choice] = 1
#
# plt.plot(weather, marker="o")
# plt.show()

# --- Q1.2 ---
# weather = np.array([])
# sunny = 0
# cloudy = 0
# rainy = 0
#
# for _ in range(N):
#     pi = np.array([1, 0, 0])
#
#     for n in range(25):
#         probs = pi @ P
#
#         # 0 for S, 1 for C, 2 for R
#         choice = np.random.choice(np.array([0, 1, 2]), p=list(probs))
#         weather = np.append(weather, choice)
#
#         # updating pi to current state
#         pi = np.zeros(3)
#         pi[choice] = 1
#
#
#     if pi[0] == 1: sunny += 1
#     elif pi[1] == 1: cloudy += 1
#     elif pi[2] == 1: rainy += 1
#
# print("Relative frequency of Sunny = ", sunny/N)
# print("Relative frequency of Cloudy = ", cloudy/N)
# print("Relative frequency of Rainy = ", rainy/N)

# --- Q1.3 ---
# get left eigenvalues and eigenvectors
# eigenvals, eigenvecs = np.linalg.eig(P.T) 
# stationary_pi = np.array([])
#
# for i in range(len(eigenvals)):
#     if 1 - 1e-3 <= eigenvals[i] <= 1 + 1e-3:
#         stationary_pi = eigenvecs[:, i]
#         stationary_pi = stationary_pi/sum(stationary_pi)
#         break
#
#
# print("Theoretical Stationary Pi:", stationary_pi)
#
# # --- Q1.4 ---
# tol = 1e-10
# n = 0
# MAX_N = int(1e+4)
#
# weather = np.array([])
#
# sunny = 0
# cloudy = 0
# rainy = 0
#
# for _ in range(N):
#     pi = np.array([1, 0, 0])
#
#     for _ in range(MAX_N):
#         probs = pi @ P
#
#         # 0 for S, 1 for C, 2 for R
#         choice = np.random.choice(np.array([0, 1, 2]), p=list(probs))
#         weather = np.append(weather, choice)
#
#         # updating pi to current state
#         pi = np.zeros(3)
#         pi[choice] = 1
#
#
# # HUHHHH?
#
#
#     if pi[0] == 1: sunny += 1
#     elif pi[1] == 1: cloudy += 1
#     elif pi[2] == 1: rainy += 1
#
# print("Relative frequency of Sunny = ", sunny/N)
# print("Relative frequency of Cloudy = ", cloudy/N)
# print("Relative frequency of Rainy = ", rainy/N)

