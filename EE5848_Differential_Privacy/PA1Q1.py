import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import HalfspaceIntersection, ConvexHull
from matplotlib.patches import Polygon

parser = argparse.ArgumentParser()
parser.add_argument("--epsilon", type=float)
parser.add_argument("--delta", type=float)
parser.add_argument("--sens", type=float)

args = parser.parse_args()
epsilon = args.epsilon
delta = args.delta
sens = args.sens

assert(epsilon > 0)
assert(delta >= 0)
assert(delta < 1)

# -- q1

# 0 < alpha < 1, 0 < beta < 1
A1 = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
v1 = np.array([[0], [1], [0], [1]])
# (epsilon, delta) constraints
A2 = np.array([[-1, -np.exp(epsilon)], [1, np.exp(epsilon)], [-np.exp(epsilon), -1], [np.exp(epsilon), 1]])
v2 = np.array([[delta - 1], [delta + np.exp(epsilon)], [delta - 1], [delta + np.exp(epsilon)]])

A = np.vstack((A1, A2))
v = np.vstack((v1, v2))

halfspaces = np.column_stack((A, -v))
interior_point = np.array([0.5, 0.5])
hs = HalfspaceIntersection(halfspaces, interior_point)
vertices = hs.intersections

print("Calculated Polygon Vertices:")
print(vertices)
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
