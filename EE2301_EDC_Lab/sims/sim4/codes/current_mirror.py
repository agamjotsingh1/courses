import numpy as np

Kp = 62.14
Id = 100e-6
Vth = 2
R1 = 1e3
V1 = Id*R1 + np.sqrt(2*Id/Kp) + Vth

print(V1)
