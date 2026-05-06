import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 10, 1000)
omega = 2 * np.pi
T = 1
phi = 0

for A in [0.5, 1, 2]:
    y = (2 * A * np.sin(omega * T / 2) / omega) * np.sin(omega * (t - T/2) + phi)
    plt.plot(t, y, label=f"A={A}")

plt.title("Effect of Amplitude A")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.grid(True)
plt.show()

