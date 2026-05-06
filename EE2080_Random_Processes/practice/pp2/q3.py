import numpy as np
import matplotlib.pyplot as plt

N = int(1e+5)
MAX_ITERS = int(1e+6)

P = np.array([[0.5, 0.5, 0, 0],
              [0.2, 0.5, 0.3, 0],
              [0, 0.3, 0.4, 0.3],
              [0.1, 0, 0.4, 0.5]])


# --- Q3.1 ---
# starting_state = np.array([1, 0, 0, 0])
# sum_hitting_times = 0
# A = [4]
#
# for _ in range(N):
#     state = starting_state
#
#     for n in range(MAX_ITERS):
#         probs = state @ P
#
#         # 0 for S, 1 for C, 2 for R
#         choice = np.random.choice(np.array([1, 2, 3, 4]), p=list(probs))
#
#         if choice in A:
#             sum_hitting_times += n + 1
#             break
#
#         # updating pi to current state
#         state = np.zeros(4)
#         state[choice - 1] = 1
#
# print("Emperical Mean for h1->4 = ", sum_hitting_times/N)


# --- Q3.2 ---
# state = np.array([0, 1, 0, 0])
# return_times = np.array([])
# n = 1
# prev_n = 0
#
# while n < MAX_ITERS:
#     probs = state @ P
#
#     # 0 for S, 1 for C, 2 for R
#     choice = np.random.choice(np.array([1, 2, 3, 4]), p=list(probs))
#
#     if choice == 2:
#         return_times = np.append(return_times, n - prev_n)
#         prev_n = n
#
#     # updating pi to current state
#     state = np.zeros(4)
#     state[choice - 1] = 1
#
#     n += 1;
#
# print("m2_hat = ", np.mean(return_times))

# # --- Q3.3 ---
# eigenvals, eigenvecs = np.linalg.eig(P.T) 
# stationary_pi = np.zeros(n)
#
# for i in range(len(eigenvals)):
#     if 1 - 1e-3 <= eigenvals[i] <= 1 + 1e-3:
#         stationary_pi = eigenvecs[:, i]
#         stationary_pi = stationary_pi/sum(stationary_pi)
#         break
#
# print("m2 = ", 1/stationary_pi[1])
