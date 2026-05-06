import numpy as np
import matplotlib.pyplot as plt

# Parameters
N_terms = 1000           # Number of Fourier series terms
T_box = 0.02           # Box kernel width
num_points = 2000      # High resolution points
L = np.pi              # Half period

# Time array
t = np.linspace(-L, L, num_points)

# Define a discontinuous, irregular waveform
# Example: step function with jumps and irregularities
irregular_wave = np.piecewise(t, [t < -np.pi/2, (t >= -np.pi/2) & (t < 0), (t >= 0) & (t < np.pi/2), t >= np.pi/2],
                              [-1, 0.5, -0.5, 1])

# Fourier series approximation
irregular_approx = np.zeros_like(t)
smoothed_irregular = np.zeros_like(t)

for n in range(1, 2*N_terms, 2):  # Only odd harmonics
    coefficient = (4 / (n * np.pi)) * (np.sin(n * np.pi/2) - np.sin(-n * np.pi/2))
    filter_factor = np.sin(n*T_box) / (n*T_box)
    irregular_approx += coefficient * np.sin(n * t)
    smoothed_irregular += coefficient * filter_factor * np.sin(n * t)

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(t, irregular_wave, color='green', label='Actual Irregular Wave', linewidth=2)
plt.plot(t, irregular_approx, label=f'Fourier Approximation (N={N_terms})', linestyle='--')
plt.plot(t, smoothed_irregular, color='orange', label='Smoothed with Frequency Domain Filter', linestyle=':')
plt.title('Irregular Discontinuous Wave Approximation and Smoothing')
plt.xlabel('t')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
