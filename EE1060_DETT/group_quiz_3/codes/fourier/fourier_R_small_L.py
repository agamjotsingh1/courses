import numpy as np
import matplotlib.pyplot as plt

alpha = 1/2
L = 10000
R = 1
w0 = 2 * np.pi
T = 2 * np.pi / w0  

t = np.linspace(0, 2, 1000)

i_dc = (10 * alpha / R) * (1 - np.exp(- (R / L) * t))

N = 10000  
sum_term = np.zeros(t.shape)

for n in range(1, N + 1):
    sum_term += np.cos((2 * np.pi * alpha - w0 * t) * n) / n**2 - (np.cos(n * w0 * t))/(n**2)

i = i_dc + (10 / (np.pi * w0 * L)) * sum_term

plt.figure(figsize=(8, 4))
plt.plot(t, i, label=r'$i(t)$ approximation', color='b')
plt.xlabel("Time (t)")
plt.ylabel("Current (i)")
plt.title("Current response for R = 1 ohm, L=10000 H, α=0.5, T=1 s")
plt.legend()
plt.grid()
plt.show()

