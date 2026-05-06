import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Set up figure
fig, ax = plt.subplots(figsize=(10, 6))

# Parameters
d = 2  # distance between plates
plate_width = 8
plate_height = 0.2

# Draw capacitor plates
plate1 = Rectangle((1, 0), plate_width, plate_height, color='gray', alpha=0.8)
plate2 = Rectangle((1, d), plate_width, plate_height, color='gray', alpha=0.8)
ax.add_patch(plate1)
ax.add_patch(plate2)

# Fill region between plates with dielectric material
dielectric = Rectangle((1, plate_height), plate_width, d-plate_height, color='lightblue', alpha=0.5)
ax.add_patch(dielectric)

# Add labels
ax.text(0.5, 0, 'z = 0', fontsize=12)
ax.text(0.5, d, 'z = d', fontsize=12)
ax.text(5, d/2, 'Dielectric material\nρ₀ C/m³\nε', fontsize=12, ha='center')

# Set axis limits and labels
ax.set_xlim(0, 10)
ax.set_ylim(-1, d+1)
ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.7)

plt.savefig("fig.png")
plt.tight_layout()
plt.show()

