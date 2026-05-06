import numpy as np
import matplotlib.pyplot as plt

N = 10

for _ in range(50):
    plt.scatter(range(N), [np.random.standard_normal() for _ in range(N)])

# N = 50
# plt.plot(range(N), [np.random.standard_normal() for _ in range(N)], marker="*")
plt.show()
