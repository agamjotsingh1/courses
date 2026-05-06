import numpy as np
import matplotlib.pyplot as plt

alpha = 1/2
R = 10000
w0 = 2 * np.pi

t = np.linspace(0, 2, 1000)
i_dc = (10 * alpha) / R

N = 10000  

sum_term = np.zeros(t.shape)

for n in range(1, N + 1):
    sum_term += np.sin((2 * np.pi * alpha - w0 * t) * n) / n + (np.sin(n * w0 * t))/n

i = i_dc + (10 / (np.pi * R)) * sum_term

plt.figure(figsize=(8, 4))
plt.plot(t, i, label=r'$i(t)$ approximation', color='b')
plt.xlabel("Time (t)")
plt.ylabel("Current (i)")
plt.title("Current reponse for R=10000 ohm, α=0.5, T= 1")
plt.legend()
plt.grid()
plt.show()

