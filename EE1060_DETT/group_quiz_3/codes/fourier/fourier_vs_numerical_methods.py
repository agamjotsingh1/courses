import matplotlib.pyplot as plt
import numpy as np
from numerical_methods import *

alpha = 0.4  # Duty cycle
T = 0.1 # time period
A = 10.0  # Amplitude
R = 1e-3
L = 1
h = T/10

t = np.arange(0, 10*T, h)
initialCurrent = 0.0

eulerCurrent = eulerMethod(R, L, T, alpha, A, t, h, initialCurrent)
rk2Current = rk2Method(R, L, T, alpha, A, t, h, initialCurrent)
rk4Current = rk4Method(R, L, T, alpha, A, t, h, initialCurrent)
reverseEulerCurrent = reverseEulerMethod(R, L, T, alpha, A, t, h, initialCurrent)
trapezoidalCurrent = trapezoidalMethod(R, L, T, alpha, A, t, h, initialCurrent)

currentFourier = current_response(t, R, L, alpha, T)

eulerError = currentFourier - eulerCurrent
rk2Error = currentFourier - rk2Current
rk4Error = currentFourier - rk4Current
trapezoidalError = currentFourier - trapezoidalCurrent
reverseEulerError = currentFourier - reverseEulerCurrent

''' Fourier vs Euler '''
plt.plot(t, currentFourier, color="blue", label="Fourier series")
plt.plot(t, eulerCurrent, color="orange", label="Euler Method")
plt.legend()
plt.savefig(f"./figs/euler_R{R}_L{L}_h{h}.png")
plt.show()

plt.plot(t, eulerError, color="green", label="Deviation of fourier vs Euler method")
plt.legend()
plt.savefig(f"./figs/eulerError_R{R}_L{L}_h{h}.png")
plt.show()

''' Fourier vs RK2 '''
plt.plot(t, currentFourier, color="blue", label="Fourier series")
plt.plot(t, rk2Current, color="orange", label="RK2 Method")
plt.legend()
plt.savefig(f"./figs/rk2_R{R}_L{L}_h{h}.png")
plt.show()

plt.plot(t, rk2Error, color="green", label="Deviation of fourier vs RK2 method")
plt.legend()
plt.savefig(f"./figs/rk2Error_R{R}_L{L}_h{h}.png")
plt.show()

''' Fourier vs RK4 '''
plt.plot(t, currentFourier, color="blue", label="Fourier series")
plt.plot(t, rk4Current, color="orange", label="RK4 Method")
plt.legend()
plt.savefig(f"./figs/rk4_R{R}_L{L}_h{h}.png")
plt.show()

plt.plot(t, rk4Error, color="green", label="Deviation of fourier vs RK4 method")
plt.legend()
plt.savefig(f"./figs/rk4Error_R{R}_L{L}_h{h}.png")
plt.show()

''' Fourier vs Reverse Euler'''
plt.plot(t, currentFourier, color="blue", label="Fourier series")
plt.plot(t, reverseEulerCurrent, color="orange", label="Reverse Euler Method")
plt.legend()
plt.savefig(f"./figs/reverseEuler_R{R}_L{L}_h{h}.png")
plt.show()

plt.plot(t, reverseEulerError, color="green", label="Deviation of fourier vs Reverse Euler method")
plt.legend()
plt.savefig(f"./figs/reverseEulerError_R{R}_L{L}_h{h}.png")
plt.show()

''' Fourier vs Trapezoidal '''
plt.plot(t, currentFourier, color="blue", label="Fourier series")
plt.plot(t, trapezoidalCurrent, color="orange", label="Trapezoidal Method")
plt.legend()
plt.savefig(f"./figs/trapezoidal_R{R}_L{L}_h{h}.png")
plt.show()

plt.plot(t, trapezoidalError, color="green", label="Deviation of fourier vs Trapezoidal method")
plt.legend()
plt.savefig(f"./figs/trapezoidalError_R{R}_L{L}_h{h}.png")
plt.show()

''' Fourier vs Everything '''
plt.plot(t, currentFourier, color="blue", label="Fourier series")
plt.plot(t, eulerCurrent, color="orange", label="Euler Method")
plt.plot(t, rk2Current, color="red", label="RK2 Method")
plt.plot(t, rk4Current, color="magenta", label="RK4 Method")
plt.plot(t, reverseEulerCurrent , color="orange", label="Reverse Euler Method")
plt.plot(t, trapezoidalCurrent, color="green", label="Trapezoidal Method")
plt.legend()
plt.savefig(f"./figs/everything_R{R}_L{L}_h{h}.png")
plt.show()

''' Deviation from fourier vs everything'''
plt.plot(t, eulerError, color="orange", label="Euler Method")
plt.plot(t, rk2Error, color="red", label="RK2 Method")
plt.plot(t, rk4Error, color="blue", label="RK4 Method")
plt.plot(t, reverseEulerError , color="magenta", label="Reverse Euler Method")
plt.plot(t, trapezoidalError, color="green", label="Trapezoidal Method")
plt.legend()
plt.savefig(f"./figs/everythingError_R{R}_L{L}_h{h}.png")
plt.show()
