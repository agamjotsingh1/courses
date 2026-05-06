Ic = 12.36e-3
Ib = 62.15e-6
beta = Ic/Ib
RL = 470
RE = 470
R1 = 18e+3
R2 = 51e+3

Re = RE*RL/(RE + RL)
Rin = 1/(1/R1 + 1/R2 + 1/(beta*beta*Re))

print(Rin)
