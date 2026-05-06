import numpy as np
import matplotlib.pyplot as plt

# Hardcoded value for alpha
alpha = 0.3

# Define the Fourier magnitude spectrum function
def fourier_spectrum(n, alpha):
    return abs(20 / (np.pi * n) * np.sin(n * np.pi * alpha))

# Define the Fourier phase spectrum function
def fourier_phase(n, alpha):
    return -np.arctan(np.tan(np.pi * n * alpha))

# Define function to plot magnitude and phase spectra
def plot_spectra():
    n = np.arange(1, 50, 1)

    # Compute magnitude and phase spectra
    magnitude = [fourier_spectrum(i, alpha) for i in n]
    phase = [fourier_phase(i, alpha) for i in n]

    # Plot Magnitude Spectrum
    plt.figure(figsize=(8, 6))
    plt.stem(n, magnitude, basefmt=" ")
    plt.title(f"Magnitude Spectrum for α = {alpha}")
    plt.xlabel("n")
    plt.ylabel("Magnitude")
    plt.grid()
    plt.show()

    # Plot Phase Spectrum
    plt.figure(figsize=(8, 6))
    plt.stem(n, phase, basefmt=" ")
    plt.title(f"Phase Spectrum for α = {alpha}")
    plt.xlabel("n")
    plt.ylabel("Phase (radians)")
    plt.grid()
    plt.show()

# Call function to plot spectra
plot_spectra()
