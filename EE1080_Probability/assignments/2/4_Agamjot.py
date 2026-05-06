import sys
import numpy as np
import scipy.stats as stats
from scipy.linalg import eigh
import matplotlib.pyplot as plt

# Ensure at least 8 arguments are provided
assert len(sys.argv) >= 8, "Too less arguments given"

# Parse mean vector and covariance matrix elements from command-line arguments
m1, m2, k1, k2, k3, k4 = [float(arg) for arg in sys.argv[1:7]]
N = int(sys.argv[7])  # Number of samples

M = np.array([m1, m2])  # Mean vector

K = np.array([[k1, k2], [k3, k4]])  # Covariance matrix

# Check symmetry of covariance matrix
assert np.array_equal(K.T, K), "K is not symmetric"

# Eigen-decomposition of K
eig_values, eig_vectors = eigh(K)

# Check if all eigenvalues are non-negative (Positive Semi-Definite)
psd = True
for eig_value in eig_values:
    if eig_value < 0:
        psd = False
        break

assert psd, "K is not Positive Semi-Definite"

# By default, numpy gives sorted eigenvalues in increasing order
# So we just reverse D and U to get ascending orderly sorted eigenvalues and eigenvectors
D = np.diag(eig_values[::-1])
U = eig_vectors[:, ::-1]

A = U@(np.sqrt(D)) # A = U(D^0.5)
S = np.random.normal(0, 1, size=(2, N))  # Standard normal samples

# Transform standard samples into desired distribution
X_samples = (A@S) + M[:, np.newaxis]

# Create meshgrid for evaluating the PDF
x1 = np.arange(-2.5, 2.5, 0.01)
x2 = np.arange(-3.5, 3.5, 0.01)
X1, X2 = np.meshgrid(x1, x2)
Xpos = np.empty(X1.shape + (2,))
Xpos[:, :, 0] = X1
Xpos[:, :, 1] = X2

# Evaluate the multivariate normal PDF on the grid
F = stats.multivariate_normal.pdf(Xpos, M, K)
X = stats.multivariate_normal.rvs(M, K, N)  # Direct sampling

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Function to plot principal directions (eigenvectors) from mean
def plot_ellipse_axis(M, U, scale=3.0, ax=None):
    if ax is None:
        ax = plt.gca()
    for i in range(2):
        direction = U[:, i] * scale
        end = M + direction
        ax.plot([M[0], end[0]], [M[1], end[1]], linestyle='--', linewidth=2, label=f"Ellipse axis {i + 1}", color="black")

# First subplot for direct sampling
axs[0].scatter(X[:, 0], X[:, 1], color="lightcoral", alpha=0.4, marker="x")
axs[0].contour(x1, x2, F, cmap="viridis")
plot_ellipse_axis(M, U, ax=axs[0])
axs[0].set_title('Multivariate Normal Samples (Direct)')
axs[0].set_xlabel('x')
axs[0].set_ylabel('y')
axs[0].legend()

# Second subplot for eigen-decomposition-based sampling
axs[1].scatter(X_samples[0], X_samples[1], color="skyblue", alpha=0.75, marker="x")
axs[1].contour(x1, x2, F, cmap="plasma")
plot_ellipse_axis(M, U, ax=axs[1])
axs[1].set_title('Multivariate Normal Samples (Eigen Decomposition)')
axs[1].set_xlabel('x')
axs[1].set_ylabel('y')
axs[1].legend()

plt.tight_layout()
plt.show()
