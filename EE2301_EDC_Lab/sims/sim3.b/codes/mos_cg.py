import numpy as np
from math import pow

Kp = 62.1464
Vth = 2

Vdd = 5
Rd = 2000
Rl = 2000
Reff = Rd*Rl/(Rd + Rl)
Vin = 2.005

# Max Vin
print(np.sqrt(2*(Vdd/Rd + Vth/Reff)/Kp) - Vth)
# Min Vin
print(-np.sqrt(2*(Vdd/Rd + Vth/Reff)/Kp) - Vth)

# Gain
# A = Kp*Reff*(3*(Vin**2) + 4*Vin*Vth + Vth**2 + 2*Vin - 2*Vth)/2
A = Kp*Reff*(-Vin + Vth)
print(A)
