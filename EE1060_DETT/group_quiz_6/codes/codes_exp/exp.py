import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

# Time setup
t = np.linspace(-5, 15, 3000)
dt = t[1] - t[0]
T = 2

# Base signal x(t) = e^(-a*t) * u(t)
def x_func(t, a):
    return np.exp(-a * t) * (t >= 0)

# Rectangular kernel functions
def h_case1(t):  # -T < t < T
    return ((t > -T) & (t < T)).astype(float)

def h_case2(t):  # 0 < t < T
    return ((t > 0) & (t < T)).astype(float)

def h_case3(t, t0):  # t0 < t < t0 + 2T
    return ((t > t0) & (t < t0 + 2 * T)).astype(float)

# Time for plotting convolution result
def get_conv_time(t):
    return np.linspace(2 * t[0], 2 * t[-1], 2 * len(t) - 1)

# ----------- CASE 1: Standard Kernel (-T, T) with varying a ------------
a_values = [-2, -1, -0.5, 0, 0.5, 1, 2]
plt.figure(figsize=(10, 5))
for a in a_values:
    x = x_func(t, a)
    h = h_case1(t)
    y = convolve(x, h, mode='full') * dt
    plt.yscale('symlog')  # handles both positive and negative values

    plt.plot(get_conv_time(t), y, label=f'a = {a}')
plt.title('Case 1: $h(t) = 1$ for $-T < t < T$ (Standard Kernel)')
plt.xlabel('Time')
plt.ylabel('Convolution Output')
plt.grid(True)
plt.legend()
plt.tight_layout()

# ----------- CASE 2: Right-Sided Kernel (0, T) with varying a ----------
plt.figure(figsize=(10, 5))
for a in a_values:
    x = x_func(t, a)
    h = h_case2(t)
    y = convolve(x, h, mode='full') * dt
    plt.yscale('symlog')  # handles both positive and negative values

    plt.plot(get_conv_time(t), y, label=f'a = {a}')
plt.title('Case 2: $h(t) = 1$ for $0 < t < T$ (Right-Sided Kernel)')
plt.xlabel('Time')
plt.ylabel('Convolution Output')
plt.grid(True)
plt.legend()
plt.tight_layout()

# ----------- CASE 3: Shifted Kernel (t0, t0 + 2T) with varying t0 ------
t0_values = [0, 2, 4]
a = 1  # fixed a
plt.figure(figsize=(10, 5))
x = x_func(t, a)
for t0 in t0_values:
    h = h_case3(t, t0)
    y = convolve(x, h, mode='full') * dt
    plt.yscale('symlog')  # handles both positive and negative values
    plt.plot(get_conv_time(t), y, label=f'$t_0$ = {t0}')
    
plt.title('Case 3: Shifted Kernel $h(t) = 1$ for $t_0 < t < t_0 + 2T$')
plt.xlabel('Time')
plt.ylabel('Convolution Output')
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()
