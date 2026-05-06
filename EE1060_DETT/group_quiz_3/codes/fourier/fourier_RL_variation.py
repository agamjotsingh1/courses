import numpy as np
import matplotlib.pyplot as plt

def compute_current(t, R, L, alpha=1/2, w0=2*np.pi, N=100):
    term1 = (10 * alpha / R) * (1 - np.exp(-R * t / L))
    series_sum = np.zeros_like(t)
    
    for n in range(1, N+1):
        sin_term = np.sin(2 * np.pi * alpha * n)
        cos_term = 1 - np.cos(2 * np.pi * alpha * n)
        denom = R**2 + (L * n * w0) ** 2
        
        term2 = (10 / (n * np.pi)) * sin_term * (
            (R * np.cos(n * w0 * t) + n * w0 * L * np.sin(n * w0 * t)) / denom
            - (R / denom) * np.exp(-R * t / L)
        )
        
        term3 = (10 / (n * np.pi)) * cos_term * (
            (R * np.sin(n * w0 * t) - L * n * w0 * np.cos(n * w0 * t)) / denom
            + (n * w0 * L / denom) * np.exp(-R * t / L)
        )
        
        series_sum += term2 + term3
    
    return term1 + series_sum

def compute_large_R_approx(t, R, alpha=1/2, w0=2*np.pi, N=100):
    term1 = 10 * alpha / R
    series_sum = np.zeros_like(t)
    
    for n in range(1, N+1):
        series_sum += (np.sin((2*np.pi*alpha - w0*t) * n) + np.sin(n*w0*t)) / n
    
    return term1 + (10 / (np.pi * R)) * series_sum

def compute_small_R_approx(t, R, L, alpha=1/2, w0=2*np.pi, N=100):
    term1 = (10 * alpha / R) * (1 - np.exp(-R * t / L))
    series_sum = np.zeros_like(t)
    
    for n in range(1, N+1):
        series_sum += (np.cos((2*np.pi*alpha - w0*t) * n) - np.cos(n*w0*t)) / (n**2)
    
    return term1 + (10 / (np.pi * w0 * L)) * series_sum

t = np.linspace(0, 5, 1000)
rl_ratios = [1/8, 1/4, 1/3, 1/2, 1, 2, 3, 4, 8]
plt.figure(figsize=(10, 6))

R = 10  # Chosen for better visualization
for rl in rl_ratios:
    L = R / rl
    i_t = compute_current(t, R, L)
    plt.plot(t, i_t, label=f'R/L={rl} (Exact)')

# Large R approximation
R_large = 1000  # Very large R
i_large_R = compute_large_R_approx(t, R_large)
plt.plot(t, i_large_R, label='Large R Approximation', color='r')

# Small R approximation
R_small = 0.1  # Very small R
L = 10  # Larger L
i_small_R = compute_small_R_approx(t, R_small, L)
plt.plot(t, i_small_R, label='Small R Approximation', color='g')

plt.xlabel('Time (s)')
plt.ylabel('Current (i)')
plt.title('Current vs Time with Different Approximations')
plt.legend()
plt.grid()
plt.ylim([0, 1])  # Increased y-scale for better visibility
plt.xlim([0,1.5])
plt.show()

