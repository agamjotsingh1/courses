import numpy as np
import matplotlib.pyplot as plt

# Parameters
time_period = 1 # Period of the square wave
max_val = 5.0      # Maximum voltage of the square wave
min_val = 0.0      # Minimum voltage of the square wave
start_val = 0.0    # Start time
end_val = 30.0     # End time
phase = 0.0        # Phase of the square wave
q0 = 0.0           # Initial charge on the capacitor
h = 0.0001           # Time step
C = 0.0001          # Capacitance in farads
R = 100          # Resistance in ohms

# Calculate the number of points
no_points = int((end_val - start_val) / h)

def square_wave(x):
    """Generate a square wave at time x."""
    return (max_val - min_val) * (np.sign(np.sin((2 * np.pi * x / time_period) + phase)) + 1)/2+ min_val

# Initialize voltage (Vq) array
Vq = np.zeros(no_points)
Vq[0] = q0 / C  # Initial voltage on the capacitor

# Time array
t = np.linspace(start_val, end_val, no_points)

# Simulate RC response using the trapezoidal method
for i in range(1, no_points):
    # Input voltage at current and previous steps
    Vin_now = square_wave(t[i])
    Vin_prev = square_wave(t[i - 1])

    # Trapezoidal update for Vq[i]
    Vq[i] = (Vq[i - 1] + (h / (2 * R * C)) * ((Vin_prev - Vq[i - 1]) + (Vin_now - Vq[i - 1]))) / (1 + h / (2 * R * C))

# Plot the result
plt.figure(figsize=(10, 6))
plt.plot(t, Vq, color='red', label='RC Response (Vq)')
#plt.plot(t, [square_wave(x) for x in t], color='blue', linestyle='--', label='Input Square Wave (Vin)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.ylim(-1,3)
plt.title('RC Circuit Response to Square Wave Input (Trapezoidal Method)')
plt.legend()
plt.grid(True)
plt.savefig('../fig.png')  # Save the figure
plt.show()

