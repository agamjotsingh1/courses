import numpy as np
import matplotlib.pyplot as plt
import math as m
from random import random as r

# Circuit parameters
R = 25   # Resistance in ohms
C = 4150e-12   # Capacitance in farads
L = 2e-3   # Inductance in henries
Vc0 = 5           # Initial capacitor voltage

a = R/L
b = 1/(L*C)
disc = (a*a/4) - b

# Simulation parameters
stepsize = 1e-9
tmax = 2e-4    # Maximum simulation time

size = int(tmax / stepsize)

t = np.linspace(0, tmax, size)

if disc < 0:
    w = np.sqrt(-disc)
    Vc = Vc0*(np.exp(-a*t/2))*(np.cos(w*t) + (a/(2*w))*(np.sin(w*t)))
elif m.fabs(disc) <= 1e-5:
    Vc = Vc0*(1+a*t/2)*(np.e**(-a*t/2))
elif disc > 0:
    w = np.sqrt(disc)
    s1 = -a/2 + w
    s2 = -a/2 - w
    A = Vc0 * s2 / (s2 - s1)
    B = Vc0 * s1 / (s1 - s2)
    Vc = A * np.e**(s1 * t) + B * np.e**(s2 * t)
vc = list()
timesample = list()

x = 0
while x<=tmax:
    timesample.append(x)
    vc.append([x,Vc0*(np.exp(-a*x/2))*(np.cos(w*x) + (a/(2*w))*(np.sin(w*x)))])
    x+=0.05e-6

print(vc[5], vc[200], vc[3000], vc[1250], vc[1729], vc[2225], vc[225], vc[400],vc[3500], vc[1000], vc[15], vc[25], vc[725], vc[1250], vc[1757], sep = "\n", end = "\n")
for _ in range(10):
    num = m.floor(r() * 4000)
    plt.scatter(vc[num][0], vc[num][1])
# Plot results
plt.plot(t, Vc)
plt.savefig("../figs/rlc.png")
plt.xlabel("Time (s)")
plt.ylabel("Voltage across capacitor (Vc)")
plt.title("Current vs. Time in an RLC Circuit")
plt.show()

