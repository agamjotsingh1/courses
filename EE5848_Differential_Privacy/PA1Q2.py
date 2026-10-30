import argparse

import numpy as np

# data -> (*xN) matrix contains vectors
# N -> dimension of feature space
# K -> number of clusters
# T -> number of iterations
# rng -> numpy rng generator (preferably seeded)
def lloyd(data, N, K, T, rng):
    rand_idx = rng.choice(data.shape[0], size=K, replace=False)
    centers = np.empty((T+1, K, N))

    centers[0] = np.copy(data[rand_idx])

    for t in range(T):
        # add a new axis and then broadcast
        distances = np.linalg.norm(data[:, np.newaxis] - centers[t], axis=2)
        labels = np.argmin(distances, axis=1)

        for k in range(K):
            cluster = data[labels == K]

            if cluster.shape[0] == 0:
                centers[t+1][k] = centers[t][k]
            else:
                centers[t+1][k] = np.mean(cluster, axis=0)/cluster.shape[0]

# old slower implementation
#         for k in range(K):
#             cluster_sum = np.zeros((1, 2))
#             cluster_len = 0
#
#             for x in data:
#                 in_cluster = True
#
#                 for j in range(K):
#                     if np.linalg.norm(x - centers[j]) > np.linalg.norm(x - centers[k]):
#                         in_cluster = False
#                         break
#
#                 if in_cluster:
#                     cluster_len += 1
#                     cluster_sum += x
#
#             new_centers[k] = 0 if cluster_len == 0 else cluster_sum/cluster_len

    return centers

parser = argparse.ArgumentParser()
parser.add_argument("--data")
parser.add_argument("--eps", default=1.0, type=float)
parser.add_argument("--T", default=20, type=int)
parser.add_argument("--K", default=4, type=int)
parser.add_argument("--seed", default=0, type=int)

args = parser.parse_args()

data = np.empty((0, 2))

# data extraction
with open(args.data, mode='r') as file:
    for line in file:
        if line.startswith("#"):
            continue

        split_line = line.strip().split(',')

        if len(split_line) != 2:
            raise ValueError("Got invalid dimensions in data (2D is required).")

        new_row = np.array([[float(n) for n in split_line]])
        data = np.append(data, new_row, axis=0)

n = data.shape[0]
rng = np.random.default_rng(seed=args.seed)

eps = args.eps
T = args.T
K = args.K

assert(eps > 0)
assert(T >= 4)
assert(K >= 2)
assert(K <= n)

eps_dash = eps/T

# sub-composition #1: computing number of elements in each class
# basically a histogram query with sens = 2
sens1 = 2
b1 = sens1/(eps_dash/2)

# sub-composition #2: computing mean of each class
# as one norm of each data is less than 1, sens is 2
sens2 = 2
b2 = sens2/(eps_dash/2)

print(f"({eps_dash}, {b1}, {b2})")

print(lloyd(data, 2, K, T, rng))
