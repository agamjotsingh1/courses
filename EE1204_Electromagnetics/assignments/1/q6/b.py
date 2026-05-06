import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')

epsilon_not = 8.85418e-12
k = 1/(4*np.pi*epsilon_not)
threshold = 1e-2

def V_Q(X, Y, q, pos):
    Rx = X - pos[0]
    Ry = Y - pos[1]
    norm = np.sqrt(Rx**2 + Ry**2)
    return k*q/norm

def V(X, Y):
    V1 = V_Q(X, Y, 1, (0, 1))
    V2 = V_Q(X, Y, 1, (0, -1))
    V3 = V_Q(X, Y, -1, (1, 0))
    V4 = V_Q(X, Y, -1, (-1, 0))
    return V1 + V2 + V3 + V4

x = np.arange(-5, 6, 0.3)
y = np.arange(-5, 6, 0.3)
X, Y = np.meshgrid(x, y)

Z = V(X, Y)

surf = ax.plot_surface(X, Y, Z, cmap='gnuplot')

fig.colorbar(surf)
plt.savefig("./b_fig.png")
plt.show()
