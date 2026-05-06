import matplotlib.pyplot as plt
import numpy as np

phi = np.arange(-20, 20, 0.1)
modF = np.sqrt((4 + 3*(np.cos(phi) + np.sin(phi)))**2 + 4)

plt.plot(phi, modF)
plt.xlabel('$\\phi$', fontsize=15)
plt.ylabel('$\\left|\\vec{F}\\right|$', fontsize=15)
plt.grid()
plt.savefig("./a_fig.png")
plt.show()
