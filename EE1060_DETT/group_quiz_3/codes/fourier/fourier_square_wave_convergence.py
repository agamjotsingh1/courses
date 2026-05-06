import matplotlib.pyplot as plt
import numpy as np

''' N -> Number of terms in fourier series '''
N_range = [2, 3, 4, 5, 6, 8, 10, 15, 20, 30, 50, 75, 100, 250, 500, 1000]
colormap = ["orange", "green", "magenta", "red"]*(len(N_range)//4 + len(N_range)%4)
alpha = 0.4
T = 1
A = 10

''' Gives the Theoretical plot for the square wave'''
def V_theory(t):
    V = []
    for instant in t:
        if instant%T <= alpha*T:
            V.append(A)
        else:
            V.append(0)
    return V

''' Gives the Simulated plot for the square wave with N = number of terms in fourier series'''
def V_sim(t, N):
    res = 10*alpha
    w_0 = 2*np.pi/T

    for n in range(1, N):
        res += (10/(np.pi*n))*( np.sin(2*np.pi*alpha*n)*np.cos(n*w_0*t) + (1 - np.cos(2*np.pi*alpha*n))*np.sin(n*w_0*t) )

    return res

t = np.arange(-0.2, 2, 0.001)

for i in range(len(N_range)):
    N = N_range[i]
    color = colormap[i]

    ''' Comparing V_sim and V_theory plots for different N'''
    plt.plot(t, V_theory(t), color="blue", label="Theoretical")
    plt.plot(t, V_sim(t, N), color=color, label=f"Fourier with N = {N}")

    plt.xlim(-0.5, 2.5)
    plt.legend()
    plt.grid()
    plt.savefig(f"./figs/convergence_n{N}.png")
    plt.show()
