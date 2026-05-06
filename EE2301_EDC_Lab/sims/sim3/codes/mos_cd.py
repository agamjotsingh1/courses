Vto = 1.38
Id = 1.1146e-3
Vg = 2.5
Vs = 1.1146

gm = 2*Id/(Vg - Vs - Vto)
Rs = 1000

print(Rs/(Rs*gm + 1))
