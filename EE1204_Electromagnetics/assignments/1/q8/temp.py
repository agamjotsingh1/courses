import numpy as np
import matplotlib.pyplot as plt

# Parameters
d = 1.0  # plate separation in arbitrary units

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Draw the capacitor plates
plate_width = 3.0
plate_thickness = 0.1

# Bottom plate at z=0
ax.fill_between([-plate_width/2, plate_width/2], 0, -plate_thickness, color='gray')
# Top plate at z=d
ax.fill_between([-plate_width/2, plate_width/2], d, d+plate_thickness, color='gray')

# Fill the region between plates with a different color to represent the material
ax.fill_between([-plate_width/2, plate_width/2], 0, d, color='lightblue', alpha=0.5)

# Add charge density representation (small + symbols scattered in the material)
np.random.seed(42)
num_charges = 100
x_charges = np.random.uniform(-plate_width/2*0.9, plate_width/2*0.9, num_charges)
z_charges = np.random.uniform(0.1, d*0.9, num_charges)

ax.scatter(x_charges, z_charges, marker='+', color='red', s=30, alpha=0.7)

# Add labels and annotations
ax.text(-plate_width/2-0.5, -plate_thickness/2, 'z = 0 (Ground)', verticalalignment='center')
ax.text(-plate_width/2-0.5, d+plate_thickness/2, 'z = d', verticalalignment='center')
ax.text(0, d/2, r'$\rho_0, \epsilon$', fontsize=14, horizontalalignment='center')

# Set axis limits and labels
ax.set_xlim(-plate_width/2-1, plate_width/2+1)
ax.set_ylim(-0.5, d+0.5)
ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_title('Parallel-Plate Capacitor with Uniform Volume Charge Density')

# Add grid and show plot
ax.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
