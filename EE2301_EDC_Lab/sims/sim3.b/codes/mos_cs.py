import numpy as np
from math import pow

Kp = 62.1464
Vth = 2
Vdd = 10
Rd = 2000
Rl = 2000
Reff = Rd*Rl/(Rd + Rl)
Vgs = 2.01

# Vgs max value
print(np.sqrt(2*Vdd/(Rd*Kp)) + Vth)

# Gain
A = Kp*Reff*(Vgs - Vth)
print(A)
