import matplotlib.pyplot as plt
import numpy as np

s = np.arange(-20, 20, 0.1)
modF = np.sqrt(4 + (40/(s**2 + 1) + 3*np.sqrt(2))**2)

plt.plot(s, modF)
plt.xlabel('$s$', fontsize=15)
plt.ylabel('$\\left|\\vec{F}\\right|$', fontsize=15)
plt.grid()
plt.savefig("./b_fig.png")
plt.show()
