import numpy as np
import matplotlib.pyplot as plt

# Function to generate a square wave burst function
def square_burst(A, T, N, t):
    """
    Generates a square wave burst.
    
    Parameters:
    A - Amplitude of the wave
    T - Period of the wave
    N - Number of cycles in the burst
    t - Current time
    
    Returns:
    Square wave value at time t
    """
    w = 2 * np.pi / T  # Angular frequency
    if t > N * T:  # Limit the burst duration
        return 0

    # Generate square wave using sign function
    return (A / 2) * np.sign(np.sin(w * t)) + (A / 2)

# Function to compute the system response
def get_response(n, h, R, C, A, T, N):
    """
    Computes the response of an RC circuit to a square wave input using numerical integration.

    Parameters:
    n - Number of time steps
    h - Time step size
    R - Resistance
    C - Capacitance
    A - Amplitude of square wave
    T - Period of square wave
    N - Number of cycles in the burst

    Returns:
    t - Time points
    y - System response at each time point
    """
    t = [0.0]  # Initialize time array
    y = [0.0]  # Initialize output response array

    for i in range(1, n):
        # Get previous and current square wave values
        v_prev = square_burst(A, T, N, t[i - 1])
        v_now = square_burst(A, T, N, t[i - 1] + h)

        # Compute next response value using numerical approximation
        y.append((y[i - 1] + (h / (2 * R * C)) * ((v_prev - y[i - 1]) + (v_now - y[i - 1]))) / (1 + h / (2 * R * C)))
        t.append(t[i - 1] + h)  # Update time step

    return t, y

# Define simulation parameters
R = 100  # Resistance in ohms
C = 1e-4  # Capacitance in farads
A = 5.0  # Amplitude of the square wave
N = 5  # Number of cycles in burst


''' BURST '''
# Case 1: T = RC
n = 100000  # Number of time steps
h = 0.00001  # Time step size
T = R * C  # Define period T as the RC time constant
plt.figure()
plt.xticks([])
plt.yticks([])
plt.plot(*get_response(n, h, R, C, A, T, N))  # Plot system response
plt.xlim(-0.02, 0.1)
plt.savefig("../figs/equals_burst_sim.png")
plt.show()

# Case 2: T >> RC (Square wave period much larger than RC time constant)
n = 100000  # Number of time steps
h = 0.0001  # Time step size
T = R * C * 100  # Increase T significantly
plt.figure()
plt.xticks([])
plt.yticks([])
plt.plot(*get_response(n, h, R, C, A, T, N))  # Plot response
plt.xlim(-0.1, 6)
plt.savefig("../figs/greater_burst_sim.png")
plt.show()

# Case 3: T << RC (Square wave period much smaller than RC time constant)
n = 100000 # Number of time steps
h = 0.00001  # Time step size
T = R * C / 10  # Decrease T significantly
plt.figure()
plt.xticks([])
plt.yticks([])
plt.plot(*get_response(n, h, R, C, A, T, N))  # Plot response
plt.xlim(-0.02, 0.06)
plt.savefig("../figs/lesser_burst_sim.png")
plt.show()

''' STEADY STATE '''
N = 10000
# Case 1: T = RC
n = 100000  # Number of time steps
h = 0.00001  # Time step size
T = R * C  # Define period T as the RC time constant
plt.figure()
plt.xticks([])
plt.yticks([])
plt.plot(*get_response(n, h, R, C, A, T, N))  # Plot system response
plt.xlim(0.1, 0.15)
plt.ylim(0, 2.5)
plt.savefig("../figs/equals_cont_sim.png")
plt.show()

# Case 2: T >> RC (Square wave period much larger than RC time constant)
n = 100000  # Number of time steps
h = 0.0001  # Time step size
T = R * C * 100  # Increase T significantly
plt.figure()
plt.xticks([])
plt.yticks([])
plt.plot(*get_response(n, h, R, C, A, T, N))  # Plot response
plt.xlim(-0.1, 6)
plt.savefig("../figs/greater_cont_sim.png")
plt.show()

# Case 3: T << RC (Square wave period much smaller than RC time constant)
n = 100000 # Number of time steps
h = 0.00001  # Time step size
T = R * C / 10  # Decrease T significantly
plt.figure()
plt.xticks([])
plt.yticks([])
plt.plot(*get_response(n, h, R, C, A, T, N))  # Plot response
plt.xlim(-0.02, 0.06)
plt.savefig("../figs/lesser_cont_sim.png")
plt.show()
