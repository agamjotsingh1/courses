import matplotlib.pyplot as plt
import numpy as np

# Parameters
total_time = 23         # Total simulation time in seconds
clock_period = 1         # Clock period
time_step = 0.01         # Time resolution

# Generate time points
time = np.arange(0, total_time, time_step)

# Ensure clock starts at 1 (to trigger falling edge first)
clock_signal = ((time + clock_period / 2) % clock_period < clock_period / 2).astype(int)

# Initialize signals
Q1 = np.zeros_like(time)
Q2 = np.zeros_like(time)
Q3 = np.zeros_like(time)

# Counter logic
counter = 0
prev_clock = 1  # Start from 1 to detect the first falling edge correctly
first_falling_edge = True  # Flag to ensure Q1 starts at 0

for i, t in enumerate(time):
    current_clock = clock_signal[i]

    # Detect falling edge (1 → 0 transition)
    if current_clock == 0 and prev_clock == 1:
        if not first_falling_edge:
            counter = (counter + 1) % 7  # Increment on subsequent falling edges
        first_falling_edge = False  # Clear the flag after the first falling edge
    prev_clock = current_clock

    # Update signals
    Q1[i] = (counter & 0b001) > 0
    Q2[i] = (counter & 0b010) > 0
    Q3[i] = (counter & 0b100) > 0

# Plotting
fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

# Clock signal
axes[0].plot(time, clock_signal, color='blue', label='Clock Signal')
axes[0].set_ylabel('Clock')
axes[0].grid(True)
axes[0].legend()

# Q1 signal
axes[1].plot(time, Q1, color='red', label='Q1')
axes[1].set_ylabel('Q1')
axes[1].grid(True)
axes[1].legend()

# Q2 signal
axes[2].plot(time, Q2, color='green', label='Q2')
axes[2].set_ylabel('Q2')
axes[2].grid(True)
axes[2].legend()

# Q3 signal
axes[3].plot(time, Q3, color='orange', label='Q3')
axes[3].set_ylabel('Q3')
axes[3].set_xlabel('Time (s)')
axes[3].grid(True)
axes[3].legend()

# Add counter state labels in the clock subplot
num_cycles = int(total_time / clock_period)
for i in range(num_cycles):
    counter_value = i % 7
    axes[0].text(i * clock_period + clock_period / 2, 1.1, f"{counter_value}",
                 horizontalalignment='center', fontsize=10, color='purple')

# Add marks at 7, 14, and 21 seconds
mark_times = [7.0, 14.0, 21.0]
for ax in axes:
    for mark in mark_times:
        ax.axvline(x=mark, color='black', linestyle='--', label=f'Mark at {mark}s')

# Improve layout
plt.tight_layout()
plt.show()
