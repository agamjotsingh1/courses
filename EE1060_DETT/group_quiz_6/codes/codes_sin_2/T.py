import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 10, 1000)
A=1
omega = 2 * np.pi
phi = 0

plt.figure()
for T in [0.5, 1, 2,3,10,15]:
    y = (2 * A * np.sin(omega * T / 2) / omega) * np.sin(omega * (t - T/2) + phi)
    plt.plot(t, y, label=f"T={T}")

plt.title("Effect of Pulse Width T")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.grid(True)
plt.show()

