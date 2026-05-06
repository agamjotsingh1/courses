import sys
import numpy as np
import matplotlib.pyplot as plt

# Set the seed for reproducibility
np.random.seed(1)

# Generate a N x n matrix with 
def gen_samples(mode, n, N, param):

    # Bernoulli Samples
    if mode == 0: 
        # param = p
        return np.random.binomial(n=1, p=param, size=(N, n)) # Binomial with n = 1, basically Bernoulli

    # Uniform Samples
    elif mode == 1:
        return np.random.uniform(0, 1, size=(N, n))

    # Exponential Samples
    elif mode == 2: 
        # param = lambda
        return np.random.exponential(scale=(1/param), size=(N, n)) # scale = 1/lambda

# Plots the gaussian pdf for respective mode and parameter
def gaussian_plot(mode, n, param):
    mean = 0 
    variance = 0

    # Bernoulli
    if mode == 0:
        # param = p
        mean = param
        variance = param*(1 - param)/n

    # Uniform
    elif mode == 1:
        mean = 1/2
        variance = (1/12)/n

    # Exponential
    elif mode == 2:
        # param = lambda
        mean = 1/param
        variance = ((1/param)**2)/n

    # Gaussian pdf
    def f(x):
        return np.exp(-(x - mean)**2/(2*variance))/(np.sqrt(2*np.pi*variance))

    # Limits for the plot
    offset = 4*np.sqrt(variance)
    x = np.arange(mean - offset, mean + offset, 0.001)
    y = f(x)

    plt.plot(x, y, color="black", label=f"N({mean}, {variance})")

mode, n, N = [int(arg) for arg in sys.argv[1:4]]

assert (mode in [0, 1, 2]), "Mode can be 0, 1, 2 only"
assert n > 0 and N > 0, "n and N have to be positive"

param = float(sys.argv[4]) if mode != 1 else 0

assert (mode == 0 and param <= 1 and param >= 0) or (mode == 1 and param > 0), "Invalid parameter"

# N x n matrix with random variable samples
X = gen_samples(mode, n, N, param)
row_averages =  [sum(X[i])/n for i in range(N)]

# Bernoulli bins are differently handled due to wierd binning issues
if mode == 0: plt.hist(row_averages, density=True, alpha=0.75, color="skyblue", label="Row Average Histogram")
else: plt.hist(row_averages, density=True, bins = int(np.sqrt(N)), alpha=0.75, color="skyblue", label="Row Average Histogram")

gaussian_plot(mode, n, param)

plt.legend()
plt.xlabel("Samples")
plt.ylabel("Frequency")

if mode == 0: plt.title(f"Bernoulli Samples (p = {param})")
elif mode == 1: plt.title("Uniform Samples ([0, 1])")
elif mode == 2: plt.title(f"Exponential Samples ($\\lambda$ = {param})")

plt.show()
