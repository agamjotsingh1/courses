import numpy as np

Id = 4.99e-5
Kp = 200e-6
W = 50e-6
L = 1e-6


lam_n = 0.01
lam_p = 0.01

ro_n = 1/(lam_n * Id)
ro_p = 1/(lam_p * Id)

gm = np.sqrt(2*Kp*(W/L)*Id)
ro = ro_n * ro_p / (ro_n + ro_p)
print("gm = ", gm)
print("ro = ", ro)
A = gm*ro
print("Gain = ", A)
