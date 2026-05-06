import math

Vdd = 3.3
mu = 273.8094484e-4
t_ox = 4.1e-9
e_ox = 3.45e-11
c_ox = e_ox / t_ox
W = 100e-6
L = 1e-6
beta = mu * c_ox * W / L
print("beta =", beta)
v_th = 0.3662473
RL = 10e3
# v_gs = v_th + (math.sqrt(1 + 2 * Vdd * beta * RL) - 1)/(beta*RL)
v_gs = v_th + (math.sqrt(1 + 4 * Vdd * beta * RL) - 1)/(2*beta*RL)

print("Optimal VGS =", v_gs)
print("VDS Swing =", v_gs - v_th, "to", Vdd)

v_ds = (v_gs - v_th + Vdd)/2
print("Optimal VDS =", v_ds)
print("Max oscillation for VDS =", Vdd - v_ds)

A = beta*(v_gs - v_th)*RL
print("Gain =", A)
v_a = (Vdd - v_ds)/A
print("Max VA =", v_a)


