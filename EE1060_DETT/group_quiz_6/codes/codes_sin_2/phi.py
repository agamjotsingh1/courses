import numpy as np
import matplotlib.pyplot as plt

A=1
t = np.linspace(0, 10, 1000)
T = 1
omega = 2 * np.pi

plt.figure()
for phi in [0, np.pi/4, np.pi/2]:
    y = (2 * A * np.sin(omega * T / 2) / omega) * np.sin(omega * (t - T/2) + phi)
    plt.plot(t, y, label=f"ϕ={phi:.2f} rad")

plt.title("Effect of Phase ϕ")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.grid(True)
plt.show()
