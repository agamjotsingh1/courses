import numpy as np
Id = 9.98e-5
lam = 0.001
ro = 1/(lam*Id)
gm = 0.0009989994994993741 # from gain code
print(20*np.log10(gm*ro))
