import numpy as np

kp = 76.2
Id = 361.7e-6
lam = 0.002
ro = 1/(lam*Id)

rl  = 1000000
reff =  ro * rl / (ro + rl)

rd = 1000
reff = rd * reff/(rd + reff)

vgs = 5 - 3.617
vto = 1.38
gm = 2 * Id / (vgs - vto)

print(gm * rd)
print(1/gm)
