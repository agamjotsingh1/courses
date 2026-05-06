import numpy as np

T = 300
k = 1.38e-23
q = 1.6e-19

Vt = k*T/q
# Id = 0.00356234
Id = 0.000119664
n = 1.752

rd = n*Vt/Id
print(Vt*n)

print(f"rd = {rd}")



