import numpy as np
import matplotlib.pyplot as plt

alpha = 1/2
L = 1
w0 = 2 * np.pi
T = 2 * np.pi / w0  

t = np.linspace(0, 2, 1000)

i_dc = (10 * alpha / L) * (1 - np.exp(-t))

N = 10000  
sum_term = np.zeros(t.shape)

for n in range(1, N + 1):
    factor = 1 / (n * np.pi * (1 + (n * w0) ** 2))
    sin_term = np.sin(2 * np.pi * alpha * n)
    cos_term = 1 - np.cos(2 * np.pi * alpha * n)

    part1 = sin_term * (np.cos(n * w0 * t) + n * w0 * np.sin(n * w0 * t) - np.exp(-t))
    part2 = cos_term * (np.sin(n * w0 * t) - n * w0 * np.cos(n * w0 * t) + n * w0 * np.exp(-t))

    sum_term += factor * (part1 + part2)

i = i_dc + (10 / L) * sum_term

plt.figure(figsize=(8, 4))
plt.plot(t, i, label=r'$i(t)$ approximation', color='b')
plt.xlabel("Time (t)")
plt.ylabel("Current (i)")
plt.title("Current response for L=1 H, α=0.5, T=1.00")
plt.legend()
plt.grid()
plt.show()

