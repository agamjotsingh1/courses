import argparse

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from scipy.spatial import ConvexHull, HalfspaceIntersection
from scipy.stats import laplace

parser = argparse.ArgumentParser()
parser.add_argument("--eps", type=float)
parser.add_argument("--delta", type=float)
parser.add_argument("--sens", type=float)

args = parser.parse_args()
eps = args.eps
delta = args.delta
sens = args.sens

assert(eps > 0)
assert(delta >= 0)
assert(delta < 1)

# -- q1

# 0 < alpha < 1, 0 < beta < 1
A1 = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
v1 = np.array([[0], [1], [0], [1]])
# (eps, delta) constraints
A2 = np.array([[-1, -np.exp(eps)], [1, np.exp(eps)], [-np.exp(eps), -1], [np.exp(eps), 1]])
v2 = np.array([[delta - 1], [delta + np.exp(eps)], [delta - 1], [delta + np.exp(eps)]])

A = np.vstack((A1, A2))
v = np.vstack((v1, v2))

halfspaces = np.column_stack((A, -v))
interior_point = np.array([0.5, 0.5])
hs = HalfspaceIntersection(halfspaces, interior_point)
vertices = hs.intersections

hull = ConvexHull(vertices)
ordered_vertices = vertices[hull.vertices]
fig, ax = plt.subplots()
poly = Polygon(ordered_vertices, facecolor='lightblue', edgecolor='blue', alpha=0.5)
ax.add_patch(poly)
ax.set_xlim(vertices[:, 0].min() - 1, vertices[:, 0].max() + 1)
ax.set_ylim(vertices[:, 1].min() - 1, vertices[:, 1].max() + 1)
ax.grid(True, linestyle='--')
ax.set_aspect('equal')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
plt.title("Region defined by Au <= v")
plt.show()

# TODO!

# -- q2
lam = delta/eps
# ystar is the threshold
# note that t is only defined from [-eps, eps] for this ystar
ystar = lambda t: (delta/2) * (1 - t/eps)
t = np.arange(-(2*eps), (2*eps), 1e-5)

# for t not in [-eps, eps]:
# a) t < -eps : At = full real set
# b) t > eps : At = null set

def alpha(t):
    if t < -eps:
        return 0.0
    elif t > eps:
        return 1.0
    else:
        return (1 - laplace.cdf(ystar(t), loc=0.0, scale=lam))

def beta(t):
    if t < -eps:
        return 1.0
    elif t > eps:
        return 0.0
    else:
        return laplace.cdf(ystar(t), loc=delta, scale=lam)

plt.figure(figsize=(8, 5))
plt.plot(t, np.vectorize(alpha)(t), label=r'$\alpha(t)$', color='blue', linewidth=2)
plt.plot(t, np.vectorize(beta)(t), label=r'$\beta(t)$', color='red', linewidth=2)

plt.title(f'Plot of $\\alpha(t)$ and $\\beta(t)$ (with $\\epsilon = {eps}$)')
plt.xlabel('t')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()

plt.show()

print("""Q2 Remarks:
    y* = delta/2 ( 1 - t/epsilon ) and laplace noise (Z) variance itself depends on delta (lam = delta/epsilon),
    so they cancel out and alpha and beta do not depend on delta at all.
""")
