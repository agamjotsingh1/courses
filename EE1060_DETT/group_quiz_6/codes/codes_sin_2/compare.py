import numpy as np
import matplotlib.pyplot as plt

# Parameters
A = 2
omega = 2 * np.pi
T = 3
phi = 5

# Time array (smaller range, fewer points)
t = np.linspace(-2, 2, 2000)

# Modified Kernel Convolution
amplitude_modified = (2 * A * np.sin(omega * T / 2)) / omega
modified_convolution = amplitude_modified * np.sin(omega * (t - T/2) + phi)

# Original Kernel Convolution
amplitude_original = (2 * A * np.sin(omega * T)) / omega
original_convolution = amplitude_original * np.sin(omega * t + phi)

# Plotting
plt.figure(figsize=(12, 6))  # Wider figure
plt.plot(t, modified_convolution, label='Modified Kernel Convolution', color='blue', alpha=0.8)
plt.plot(t, original_convolution, label='Original Kernel Convolution', color='red', alpha=0.8)
plt.title('Comparison of Convolution Results')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.show()
