import numpy as np
import matplotlib.pyplot as plt

# Parameters
N_terms = 10           # Number of Fourier series terms
T_box = 0.02           # Box kernel width
num_points = 2000      # High resolution points
L = np.pi              # Half period

# Time array
t = np.linspace(-L, L, num_points)

# Build triangular wave using Fourier series approximation
tri_approx = np.zeros_like(t)
smoothed_tri = np.zeros_like(t)

for n in range(1, 2*N_terms, 2):  # Only odd harmonics
    coefficient = (8 / (np.pi**2)) * ((-1)**((n-1)//2)) / (n**2)
    filter_factor = np.sin(n*T_box) / (n*T_box)
    tri_approx += coefficient * np.sin(n * t)
    smoothed_tri += coefficient * filter_factor * np.sin(n * t)

# Actual triangular wave for reference
tri_actual = 2 * np.abs(t/np.pi) - 1

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(t, tri_actual, color='green', label='Actual Triangular Wave', linewidth=2)
plt.plot(t, tri_approx, label=f'Fourier Approximation (N={N_terms})', linestyle='--')
plt.plot(t, smoothed_tri, color='orange', label='Smoothed with Frequency Domain Filter', linestyle=':')
plt.title('Triangular Wave Approximation and Smoothing')
plt.xlabel('t')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
