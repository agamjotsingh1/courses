import matplotlib.pyplot as plt
import numpy as np

''' N -> Number of terms in fourier series '''
N_range = [2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 75, 100, 250, 500, 1000]  # Different values of N to test
colormap = ["orange", "green", "magenta", "red"]*(len(N_range)//4 + len(N_range)%4)  # Create a repeating color pattern
alpha = 0.4  # Duty cycle of the square wave (40%)
T = 1  # Period of the square wave
A = 10  # Amplitude of the square wave

def V_theory(t):
    """
    Generate the theoretical square wave with amplitude A and duty cycle alpha.
    
    Args:
        t: Array of time points
    
    Returns:
        Array of voltage values representing the square wave
    """
    V = []
    for instant in t:
        if instant%T <= alpha*T:  # If within the duty cycle portion
            V.append(A)  # High voltage
        else:
            V.append(0)  # Low voltage (0)
    return V

def V_sim(t, N):
    """
    Calculate the Fourier series approximation of the square wave.
    
    Args:
        t: Array of time points
    
    Returns:
        Array of voltage values from the Fourier approximation
    """
    res = 10*alpha  # Result of the fourier series upto N
    w_0 = 2*np.pi/T  # Angular frequency
    
    for n in range(1, N):
        # This implements the Fourier series for a square wave with arbitrary duty cycle
        res += (10/(np.pi*n))*( np.sin(2*np.pi*alpha*n)*np.cos(n*w_0*t) + (1 - np.cos(2*np.pi*alpha*n))*np.sin(n*w_0*t) )

    return res

# Create time array from -0.2 to 2 seconds with 0.001 second steps
t = np.arange(-0.2, 2, 0.001)

# Loop through different values of N
for i in range(len(N_range)):
    N = N_range[i]  # Current number of terms
    color = colormap[i]  # Select color for this plot

    ''' Comparing V_sim and V_theory plots for different N'''
    plt.plot(t, V_theory(t), color="blue", label="Theoretical")  # Plot the theoretical square wave
    plt.plot(t, V_sim(t, N), color=color, label=f"Fourier with N = {N}")  # Plot the Fourier approximation

    plt.xlim(-0.5, 2.5)  # Set x-axis limits
    plt.legend()  # Show legend
    plt.grid()  # Display grid
    plt.savefig(f"./figs/convergence_n{N}.png")  # Save figure to file
    plt.show()  # Display the plot

