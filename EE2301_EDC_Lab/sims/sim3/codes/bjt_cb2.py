Ic = 1.376e-3
Ib = 6.566e-6
Ie = 1.383e-3
Vt = 25.875e-3
beta = Ic/Ib
re = Vt/Ie
Re = 750
RB1 = 56e+3
RB2 = 12e+3
Rin = 1/(1/RB1 + 1/RB2 + 1/(beta*(Re + re)))

print(Rin)
print(beta*re)

# redash || re
print(re*Re/(re + Re))

RC = 2200
RL = 10e+3

print(RC*RL/((RC + RL)*re))
