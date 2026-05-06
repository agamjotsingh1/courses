import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Define the hemisphere parameters
r = 1  # Radius of the hemisphere
theta = np.linspace(0, np.pi / 2, 20)  # Polar angle (sparser grid for field lines)
phi = np.linspace(0, 2 * np.pi, 20)   # Azimuthal angle (sparser grid for field lines)

# Create a meshgrid for theta and phi
theta, phi = np.meshgrid(theta, phi)

# Parametric equations for the hemisphere
x = r * np.sin(theta) * np.cos(phi)
y = r * np.sin(theta) * np.sin(phi)
z = r * np.cos(theta)

# Create the circular base in the xy-plane
circle_theta = np.linspace(0, 2 * np.pi, 200)  # Increased resolution for smoothness
circle_x = r * np.cos(circle_theta)
circle_y = r * np.sin(circle_theta)
circle_z = np.zeros_like(circle_x)

# Set up the figure and axis
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Plot the hemisphere surface with higher resolution
ax.plot_surface(x, y, z, color='b', alpha=0.6, edgecolor='k')

# Plot the circular base with higher resolution
ax.plot(circle_x, circle_y, circle_z, color='black', linewidth=2)

# Define field lines (flux density field F₁ = 5aₓ) originating from points on the hemisphere
U_field = np.zeros_like(x)  # No x-component of F₁/F₂
V_field = np.zeros_like(y)  # No y-component of F₁/F₂
W_field = 5 * np.ones_like(z)  # Constant z-component of F₁/F₂

# Add quiver plot for field lines originating from the hemisphere surface
ax.quiver(x[::4], y[::4], z[::4], U_field[::4], V_field[::4], W_field[::4], length=0.2, normalize=True, color='red', alpha=0.5, label="$F_1 = 5\\mathbf{a_z}$")

# Set labels and title
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')
ax.set_zlabel('Z-axis')

# Set aspect ratio
ax.set_box_aspect([1, 1, 1])

plt.legend()
plt.savefig("fig.png")
plt.show()
