import numpy as np

# Mosfet Params
lam = 0.002
Vth = 1.38
Kp = 76.2

# DC Params
Id = 6.63e-3
Vg = 8.0232
Vs = 6.63

gm = 2*Id/(Vg - Vs - Vth)
rd = 80

print(gm*rd)
