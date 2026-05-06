import numpy as np
T = 300
k = 1.38e-23
q = 1.6e-19

Vt = k*T/q
Vce = 0.0184504
Vbe = 0.779257

Ib = 22e-3
Ic = 4.96e-3
Ie = 120.43e-3

rpi = Vt/Ib
re = Vt/Ie
gm = Ic/Vt

print(f"Vt = {Vt}")
print(f"rpi = {rpi}")
print(f"gm = {gm}")
print(f"re = {re}")
#
# V(n004):	 0.779257	 voltage
# V(n003):	 5	 voltage
# V(n002):	 0.0184504	 voltage
# V(n001):	 5	 voltage
# Ic(Q1):	 0.00498155	 device_current
# Ib(Q1):	 0.00422074	 device_current
# Ie(Q1):	 -0.00920229	 device_current
# Is(Q1):	 0	 device_current
# I(VBE):	 -0.00422074	 device_current
# I(R1):	 -0.00422074	 device_current
# I(VCC):	 -0.00498155	 device_current
# I(RC):	 0.00498155	 device_current

