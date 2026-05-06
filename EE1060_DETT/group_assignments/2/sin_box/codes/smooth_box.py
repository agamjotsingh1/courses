import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

# Function to create different types of noisy curves
def generate_noisy_curve(t, curve_type='sin'):
    if curve_type == 'sin':
        curve = np.sin(2 * np.pi * 0.5 * t)
    elif curve_type == 'step':
        curve = np.heaviside(t - 5, 1)
    elif curve_type == 'square':
        curve = np.sign(np.sin(2 * np.pi * 0.5 * t))
    elif curve_type == 'ramp':
        curve = t
    elif curve_type == 'decay':
        curve = np.exp(-0.5 * t)
    elif curve_type == 'gaussian':
        curve = np.exp(-((t-5)**2)/2)
    else:
        curve = np.zeros_like(t)

    noise = np.random.normal(0, 0.02, size=t.shape)
    return curve + noise

# Define box kernels
def full_box_kernel(T, dt):
    width = int(T/dt)
    if width % 2 == 0:
        width += 1  # make odd for symmetry
    kernel = np.ones(width)
    kernel /= kernel.sum()  # normalize
    return kernel

# Parameters
dt = 0.0001
t = np.arange(0, 10, dt)
T = 0.1  # fixed T for smoothing
curve_types = ['sin', 'step', 'square', 'ramp', 'decay', 'gaussian']

# Generate and plot for each curve separately
for curve_type in curve_types:
    noisy_curve = generate_noisy_curve(t, curve_type)
    kernel = full_box_kernel(T, dt)
    smoothed_curve = convolve(noisy_curve, kernel, mode='same')

    plt.figure(figsize=(10, 4))
    plt.plot(t, noisy_curve, label=f'Noisy {curve_type.capitalize()}', color='red')
    plt.plot(t, smoothed_curve, label=f'Improved {curve_type.capitalize()}', color='blue')
    plt.title(f'Smoothing of Noisy {curve_type.capitalize()} with Full Box Kernel (T={T})')
    plt.xlabel('Time t')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"./figs/noisy_{curve_type}_plot.png")
    plt.show()
