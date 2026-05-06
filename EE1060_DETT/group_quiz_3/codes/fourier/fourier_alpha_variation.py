import numpy as np
import matplotlib.pyplot as plt

# Given parameters
R = 10  # Resistance in ohms
L = 1   # Inductance in Henrys
V0 = 10  # Voltage
omega0 = 2 * np.pi  # Angular frequency
t = np.linspace(0, 2, 1000)  # Time range

# Function to compute current i(t) for a given alpha
def compute_current(alpha, t, N=50):
    i_t = (V0 * alpha / R) * (1 - np.exp(-R * t / L))
    sum_term = np.zeros_like(t)
    
    for n in range(1, N + 1):
        sin_term = np.sin(2 * np.pi * alpha * n)
        cos_term = np.cos(2 * np.pi * alpha * n)

        coeff1 = (10 / (n * np.pi)) * sin_term
        coeff2 = (10 / (n * np.pi)) * (1 - cos_term)

        term1 = coeff1 * ((R * np.cos(n * omega0 * t) + n * omega0 * L * np.sin(n * omega0 * t)) / (R**2 + L**2 * (n * omega0)**2) 
                          - (R / (R**2 + L**2 * (n * omega0)**2)) * np.exp(-R * t / L))
        
        term2 = coeff2 * ((R * np.sin(n * omega0 * t) - L * n * omega0 * np.cos(n * omega0 * t)) / (R**2 + L**2 * (n * omega0)**2) 
                          + (n * omega0 * L / (R**2 + L**2 * (n * omega0)**2)) * np.exp(-R * t / L))

        sum_term += term1 + term2
    
    return i_t + sum_term

# Define alpha values, including the small alpha case
alpha_values = [0.1 / (2 * np.pi), 1/8, 1/4, 1/2, 3/4, 7/8, 1]
colors = ['k', 'b', 'g', 'r', 'c', 'm', 'y']  # Different colors for curves

# Plot all curves in one figure
plt.figure(figsize=(10, 5))

for alpha, color in zip(alpha_values, colors):
    i_t = compute_current(alpha, t)
    plt.plot(t, i_t, label=fr'$\alpha = {alpha:.4f}$', color=color)

plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.title("Current in RL Circuit for Different α Values (Including Small Alpha Case)")
plt.legend()
plt.grid(True)
plt.show()

