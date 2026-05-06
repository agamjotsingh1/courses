import numpy as np
import matplotlib.pyplot as plt

# Parameters
N_terms = 100           # Number of Fourier series terms
T_box = 0.02           # Box kernel width
num_points = 2000      # High resolution points
L = 3*np.pi              # Half period

# Time array
t = np.linspace(-L, L, num_points)

# Build square wave using Fourier series approximation
square_approx = np.zeros_like(t)
smoothed_square = np.zeros_like(t)

for n in range(1, 2*N_terms, 2):  # Only odd harmonics
    coefficient = (4/np.pi) * (1/n)
    filter_factor = np.sin(n*T_box) / (n*T_box)
    square_approx += coefficient * np.sin(n * t)
    smoothed_square += coefficient * filter_factor * np.sin(n * t)

# Actual square wave for reference
square_actual = np.sign(np.sin(t))

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(t, square_actual, color='red', label='Actual Square Wave', linewidth=2)
plt.plot(t, square_approx, label=f'Fourier Approximation (N={N_terms})', color="blue", linewidth=2)
plt.plot(t, smoothed_square, color='orange', label='Smoothed with Box Kernel')
plt.title('Square Wave Approximation and Smoothing')
plt.xlabel('t')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig(f"./figs/fourier_box_N{N_terms}.png")
plt.show()

