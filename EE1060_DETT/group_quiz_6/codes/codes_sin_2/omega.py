import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 10, 1000)
A = 1
T = 1
phi = 0

plt.figure()
for omega in [np.pi, 2*np.pi, 4*np.pi]:
    y = (2 * A * np.sin(omega * T / 2) / omega) * np.sin(omega * (t - T/2) + phi)
    plt.plot(t, y, label=f"ω={omega:.1f}")

plt.title("Effect of Angular Frequency ω")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.grid(True)
plt.show()


