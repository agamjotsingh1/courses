import random
import sys
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

random.seed(42) # Sets the seed for reproducibility

# Convert I matrix to a decimal representation
# Columns in I are the binary representation
def I_to_decimal(I):
    n = len(I)
    N = len(I[0])

    decimal_I = [] # Decimal I matrix, array of size (N x 1)

    for j in range(N):
        decimal = 0
        
        # Converting the column to 
        for i in range(n):
            if(I[i][j]):
                decimal += 2**i

        decimal_I.append(decimal)

    return decimal_I

# Generates a U matrix of size (n x N)
# with uniform random variable sample as each entry
def gen_U(n, N):
    U = [[random.uniform(0, 1) for _ in range(N)] for _ in range(n)]
    return U

# Generates the I Matrix from the given U matrix
# k subsets are represented as binary representation in columns of I
def gen_I(U, k):
    n = len(U)
    N = len(U[0])

    # Creates a matrix of (n x N) with all entries as 0
    I = [[0 for _ in range(N)] for _ in range(n)]

    # Applying the algorithm given in the problem statement
    for j in range(N):
        for i in range(n):
            prev_sum = 0
            for a in range(i):
                prev_sum += I[a][j]

            I[i][j] = 1 if U[i][j] <= (k - prev_sum)/(n - i) else 0

    return I

# Finally generate the decimal representation of selected k subsets of n
def gen_k_subsets(n, k, N):
    U = gen_U(n, N)
    I = gen_I(U, k)
    return I_to_decimal(I)

n, k, N = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]) # Accept arguments from CLI
assert n > 0 and k >= 0 and N >= 0, "Negative parameters not allowed"
assert k <= n, "k should always be less than or equal to n"

distribution = gen_k_subsets(n, k, N)
plt.hist(distribution, bins=2**n, range=(0, 2**n)) # Number of bins 
plt.xlabel("Decimal representation of subsets")
plt.ylabel("Frequency")
plt.title(f"Generating {k} (k) subsets for {n} (n)")
plt.show()
