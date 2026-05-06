import numpy as np
import matplotlib.pyplot as plt

# Time range
t = np.linspace(0, 5, 1000)

# Define 7 parameter sets: A, omega (ω), T, phi (ϕ)
parameter_sets = [
    {"A": 1, "omega": 2 * np.pi, "T": 1, "phi": 0},
    {"A": 2, "omega": np.pi, "T": 0.5, "phi": np.pi/4},
    {"A": 0.5, "omega": 3 * np.pi, "T": 1.5, "phi": np.pi/2},
    {"A": 1.5, "omega": 4 * np.pi, "T": 2, "phi": np.pi},
    {"A": 1, "omega": np.pi/2, "T": 0.8, "phi": -np.pi/2},
    {"A": 0.8, "omega": 5 * np.pi, "T": 1.2, "phi": np.pi/3},
    {"A": 1.2, "omega": np.pi/3, "T": 0.6, "phi": -np.pi/4},
]

# Plotting
plt.figure(figsize=(12, 8))
for i, params in enumerate(parameter_sets):
    A = params["A"]
    omega = params["omega"]
    T = params["T"]
    phi = params["phi"]
    
    y = (2 * A * np.sin(omega * T / 2) / omega) * np.sin(omega * (t - T / 2) + phi)
    plt.plot(t, y, label=f"Set {i+1}: A={A}, ω={omega:.2f}, T={T}, ϕ={phi:.2f}")

plt.title("Convolved Output y(t) for 7 Parameter Sets")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

