import numpy as np
import matplotlib.pyplot as plt

n = 3
filename = f'output_sig{n}.txt'  
filename_figs = f'output_sig{n}.png'  
FRACTIONAL_BITS = 14

try:
    raw_integers = np.loadtxt(filename)
    scaled_data = raw_integers / (2 ** FRACTIONAL_BITS)

    plt.figure(figsize=(10, 5))
    plt.plot(scaled_data, linewidth=1.5)
    
    plt.title(f"FIR Filter Output ({filename})")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename_figs)
    plt.show()

except FileNotFoundError:
    print(f"Error: Could not find '{filename}'. Check the path.")
except Exception as e:
    print(f"An error occurred: {e}")
