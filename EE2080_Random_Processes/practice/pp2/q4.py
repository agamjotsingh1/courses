import numpy as np
import matplotlib.pyplot as plt


MAX_ITERS = int(1e+6)

P = np.array([[0, 0.5, 0.5, 0, 0, 0],
              [0.2, 0, 0.8, 0, 0, 0],
              [0, 0, 0, 0.5, 0.5, 0],
              [0, 0, 0, 0, 0.4, 0.6],
              [0, 0, 0, 0.5, 0, 0.5],
              [0, 0, 0, 0.3, 0.7, 0]])

# --- Q4.1 ---
# N = 500
# T = 10
#
# starting_state = np.ones(6)/6
# trajectories = np.zeros((N, T))
#
# for i in range(N):
#     state = starting_state
#
#     for n in range(T):
#         probs = state @ P
#
#         # 0 for S, 1 for C, 2 for R
#         choice = np.random.choice(np.array([1, 2, 3, 4, 5, 6]), p=list(probs))
#
#         trajectories[i][n] = choice
#
#         # updating pi to current state
#         state = np.zeros(6)
#         state[choice - 1] = 1
#
# R = np.zeros((6, 6))
#
# for traj in trajectories:
#     for i in range(10):
#         for j in range(9, i - 1, -1):
#             R[int(traj[i] - 1)][int(traj[j] - 1)] = 1
#
# print(R)
# comm_classes = []
# for i in range(6):
#     if len(comm_classes) == 0:
#         comm_classes.append([i + 1,])
#         continue
#
#     is_found = 0
#     for j in range(len(comm_classes)):
#         comm_class = comm_classes[j]
#
#         for ele in comm_class:
#             if R[i][ele - 1] == 1 and R[ele - 1][i] == 1:
#                 comm_classes[j].append(i + 1)
#                 is_found = 1
#                 break
#
#         if(is_found): break
#
#     if not is_found:
#         comm_classes.append([i+1,])
#
# print(comm_classes)
#
# --- Q4.2 ---
N = 500
T = 10

trajectories = np.zeros((N, T))

for state_to_check in range(1, 7):
    starting_state = np.zeros(6)
    starting_state[state_to_check - 1] = 1
    num_returns = 0

    for i in range(N):
        state = starting_state

        for n in range(T):
            probs = state @ P

            # 0 for S, 1 for C, 2 for R
            choice = np.random.choice(np.array([1, 2, 3, 4, 5, 6]), p=list(probs))

            if choice == state_to_check:
                num_returns += 1
                break

            # updating pi to current state
            state = np.zeros(6)
            state[choice - 1] = 1

    print(num_returns/N)
    if num_returns/N < 1 - 1e-2: print(f"State {state_to_check} -> Transient")
    else: print(f"State {state_to_check} -> Recurrent")

