import matplotlib.pyplot as plt
import numpy as np

epsilon_not = 8.85418e-12
k = 1/(4*np.pi*epsilon_not)

def E_Q(X, Y, q, pos):
    Rx = X - pos[0]
    Ry = Y - pos[1]
    norm = np.sqrt(Rx**2 + Ry**2)
    return k*q*(X - pos[0])/norm**3, k*q*(Y - pos[1])/norm**3

def E(X, Y):
    E1 = E_Q(X, Y, 1, (0, 1))
    E2 = E_Q(X, Y, 1, (0, -1))
    E3 = E_Q(X, Y, -1, (1, 0))
    E4 = E_Q(X, Y, -1, (-1, 0))
    return E1[0] + E2[0] + E3[0] + E4[0], E1[1] + E2[1] + E3[1] + E4[1]

x = np.linspace(-3, 3, 20)
y = np.linspace(-3, 3, 20)
X, Y = np.meshgrid(x, y)

U, V = E(X, Y)

magnitude = np.sqrt(U**2 + V**2)
U[U < magnitude] = np.nan

U_norm = U / magnitude
V_norm = V / magnitude

plt.figure(figsize=(6, 6))
quiver_plot = plt.quiver(X, Y, U_norm, V_norm, magnitude, cmap='gnuplot')
plt.colorbar(quiver_plot, label='Electric Field Magnitude')
plt.savefig("./a_fig.png")
plt.show()
