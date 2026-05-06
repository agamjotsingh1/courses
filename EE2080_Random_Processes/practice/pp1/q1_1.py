import numpy as np
import matplotlib.pyplot as plt

N = 50

def gen_process_path():
    theta = np.random.uniform(0, 2*np.pi)
    return [ np.cos((np.pi*n/5) + theta) for n in range(N) ]

for _ in range(1):
    path = gen_process_path()
    plt.plot(range(N), path, marker="o")

plt.show()
