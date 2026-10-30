import argparse
import csv

import numpy as np

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
np.random.seed(args.seed)

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
