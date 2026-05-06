
import numpy as np
import matplotlib.pyplot as plt

# Parameters
A = 1.0          # Amplitude of sine wave
omega = 1.0      # Angular frequency
phi = 0.0        # Phase
T = 2.0          # Half-width of rectangular kernel
tau_0 = 3.0      # Shift of rectangular kernel
t_min = -4*T      # Minimum time for plotting
t_max = 4*T       # Maximum time for plotting
dt = 0.01        # Time step

# Create time array
t = np.arange(t_min, t_max, dt)

# Input signal f(t) = A*sin(omega*t + phi)
f_t = A * np.sin(omega * t + phi)

# Analytical solution for convolution with shifted rectangular kernel
scaling_factor = 2*A*np.sin(omega*T)/omega
y_analytical = scaling_factor * np.sin(omega*(t-tau_0) + phi)

# Plot 1: Original signal vs convolved output on one plot
plt.figure(figsize=(12, 6))
plt.plot(t, f_t, 'b-', label='Original Signal: $f(t) = A\\sin(\\omega t + \\phi)$')
plt.plot(t, y_analytical, 'r-', label=f'Convolved Output: T = {T}, $\\tau_0$ = {tau_0}, $\\omega$={omega}')
plt.title('Comparison: Original Signal vs Convolution Output')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.savefig('./figs/original_vs_convolved.png', dpi=300)
plt.show()

# Plot 2: Effect of varying T
plt.figure(figsize=(12, 6))
T_values = [0.5, 1.0, 2.0]
for T_val in T_values:
    scaling_factor = 2*A*np.sin(omega*T_val)/omega
    y_T = scaling_factor * np.sin(omega*(t-tau_0) + phi)
    plt.plot(t, y_T, label=f'T = {T_val}, Scale = {scaling_factor:.2f}')

plt.title('Effect of Kernel Width (T) on Convolution Output')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.savefig('./figs/varying_T_effect.png', dpi=300)
plt.show()

# Plot 2.1: Effect of varying T at n*pi
plt.figure(figsize=(12, 6))
T_values = [1*np.pi, 2*np.pi, 3*np.pi]
plt.plot(t, np.sin(omega*(t-tau_0) + phi), label=f'Original Signal')

for T_val in T_values:
    scaling_factor = 2*A*np.sin(omega*T_val)/omega
    y_T = scaling_factor * np.sin(omega*(t-tau_0) + phi)
    plt.plot(t, y_T, label=f'Convolved Signal, T = {int(T_val/np.pi)} $\\pi$, Scale = {scaling_factor:.2f}')

plt.title('Effect of Kernel Width (T) at T = n$\\pi$ on Convolution Output')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.savefig('./figs/varying_T_pi_effect.png', dpi=300)
plt.show()

# Plot 3: Effect of varying tau_0
plt.figure(figsize=(12, 6))
tau_values = [0.0, 2.0, 4.0]
for tau_val in tau_values:
    y_tau = (2*A*np.sin(omega*T)/omega) * np.sin(omega*(t-tau_val) + phi)
    plt.plot(t, y_tau, label=f'$\\tau_0$ = {tau_val}')

plt.title('Effect of Kernel Shift ($\\tau_0$) on Convolution Output')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.savefig('./figs/varying_tau_effect.png', dpi=300)
plt.show()

# Plot 4: Effect of varying omega
plt.figure(figsize=(12, 6))
omega_values = [0.5, 1.0, 2.5]
for omega_val in omega_values:
    scaling_factor = 2*A*np.sin(omega_val*T)/omega_val
    y_omega = scaling_factor * np.sin(omega_val*(t-tau_0) + phi)
    plt.plot(t, y_omega, label=f'$\\omega$ = {omega_val}, Scale = {scaling_factor:.2f}')

plt.title('Effect of Angular Frequency ($\\omega$) on Convolution Output')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.savefig('./figs/varying_omega_effect.png', dpi=300)
plt.show()

# Plot 5: Scaling factor vs omega
plt.figure(figsize=(12, 6))
omega_values = np.linspace(0.1, 20, 1000)
scaling_factors = 2*np.sin(omega_values)/omega_values

plt.plot(omega_values, scaling_factors)
plt.title('Scaling Factor $\\frac{2\\sin(\\omega T)}{\\omega}$ vs $\\omega$, T = 1 s')
plt.xlabel('$\\omega$')
plt.ylabel('Scaling Factor')
plt.grid(True)

# Mark zeros of the scaling factor
zeros = np.pi * np.arange(1, 7)
plt.plot(zeros, np.zeros_like(zeros), 'ro', label='Zeros at $\\omega T = n\\pi$')
plt.legend()
plt.savefig('./figs/scaling_factor_analysis.png', dpi=300)
plt.show()

# Plot 5.1: Scaling factor vs T
plt.figure(figsize=(12, 6))
T_vals = np.linspace(0.1, 20, 1000)
scaling_factors = 2*np.sin(T_vals) # omega = 1

plt.plot(T_vals, scaling_factors)
plt.title('Scaling Factor $\\frac{2\\sin(\\omega T)}{\\omega}$ vs $T$, $\\omega$ = 1 rad/s')
plt.xlabel('$T$')
plt.ylabel('Scaling Factor')
plt.grid(True)
plt.legend()
plt.savefig('./figs/scaling_factor_analysis_T.png', dpi=300)
plt.show()


