import numpy as np

Id = 1e-6
Kp = 62.1464
Vth = 2
# Vgs = np.sqrt(2*(Id/Kp)) + Vth
# Vgs = -2.0001793
Vin = -2.00017
lam = 0.001
# print(Vgs)

# Range of Vin
print(-np.sqrt(2*Id/Kp) - Vth, " to ", -Vth)
print("gain = ", 1-2/(lam*(Vin + Vth)))
