import numpy as np
import matplotlib.pyplot as plt

# Configuration
T_values = [1, 2, 3]  # Kernel widths to compare
tau0 = 1               # Time shift for Case 3
t = np.linspace(-5, 5, 1000)  # Time axis

# 1. Standard Kernel Plot (-T ≤ t ≤ T)
plt.figure(figsize=(10, 5))
for T in T_values:
    y = np.piecewise(t,
        [t < -T, (-T <= t) & (t <= T), t > T],
        [0, lambda t: t + T, 2*T]
    )
    plt.plot(t, y, linewidth=2, label=f'T = {T}')

plt.title('Case 1: Standard Kernel ($-T \leq t \leq T$)')
plt.xlabel('Time')
plt.ylabel('Output $y(t)$')
plt.grid(True)
plt.legend()
plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 2. Causal Kernel Plot (0 ≤ t ≤ T)
plt.figure(figsize=(10, 5))
for T in T_values:
    y = np.piecewise(t,
        [t < 0, (0 <= t) & (t <= T), t > T],
        [0, lambda t: t, T]
    )
    plt.plot(t, y, linewidth=2, label=f'T = {T}')

plt.title('Case 2: Causal Kernel ($0 \leq t \leq T$)')
plt.xlabel('Time')
plt.ylabel('Output $y(t)$')
plt.grid(True)
plt.legend()
plt.axvline(x=0, color='gray', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 3. Shifted Kernel Plot (-T+τ₀ ≤ t ≤ T+τ₀)
plt.figure(figsize=(10, 5))
for T in T_values:
    y = np.piecewise(t,
        [t < -T + tau0, (-T + tau0 <= t) & (t <= T + tau0), t > T + tau0],
        [0, lambda t: t - tau0 + T, 2*T]
    )
    plt.plot(t, y, linewidth=2, label=f'T = {T} ($τ_0$ = {tau0})')

plt.title(f'Case 3: Shifted Kernel ($-T+τ_0 \leq t \leq T+τ_0$)')
plt.xlabel('Time')
plt.ylabel('Output $y(t)$')
plt.grid(True)
plt.legend()
plt.axvline(x=tau0, color='gray', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()