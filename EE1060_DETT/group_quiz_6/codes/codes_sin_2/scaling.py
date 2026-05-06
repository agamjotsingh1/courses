import numpy as np
import matplotlib.pyplot as plt

omega = np.linspace(0.01, 10, 1000)  # Avoid division by zero

T_values = [0.5, 1, 1.5, 2, 3, 4]

plt.figure(figsize=(10, 6))

for T in T_values:
    amplitude_ratio = (2 * np.sin(omega * (T/2))) / omega
    plt.plot(omega, amplitude_ratio, label=f"T = {T}")

plt.title("Amplitude Ratio (A_modified / A) vs Angular Frequency (ω)")
plt.xlabel("ω (Angular Frequency)")
plt.ylabel("A_modified / A")
plt.grid(True)
plt.legend()
plt.show()

