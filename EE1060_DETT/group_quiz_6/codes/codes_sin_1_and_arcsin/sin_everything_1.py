import numpy as np
import matplotlib.pyplot as plt
import os

if not os.path.exists('figures'):
    os.makedirs('figures')

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 13,
    'figure.figsize': (8, 5),
    'lines.linewidth': 2
})

A = 1.0
omega = 2.0
phi = 0.0
T = 1.0
t = np.linspace(-5, 5, 1000)

def inputSignal(t, A, omega, phi):
    return A * np.sin(omega * t + phi)

def rectKernel(t, T):
    return np.where((t >= -T) & (t <= T), 1, 0)

def convResult(t, A, omega, phi, T):
    return (2*A/omega) * np.sin(omega*T) * np.sin(omega*t + phi)

def plotAmplitudeEffect():
    A_values = [0.5, 1.0, 2.0]
    fig, ax = plt.subplots()
    for A_val in A_values:
        ax.plot(t, convResult(t, A_val, omega, phi, T), label=f'A = {A_val}')
    ax.set(xlabel='Time (t)', ylabel='Output y(t)', title='Amplitude Effect')
    ax.legend()
    plt.savefig('figures/amplitude_effect.png', dpi=300)
    plt.close()

def plotFrequencyEffect():
    omega_values = [1.0, 2.0, 3.0]
    fig, ax = plt.subplots()
    for omega_val in omega_values:
        ax.plot(t, convResult(t, A, omega_val, phi, T), label=f'ω = {omega_val}')
    ax.set(xlabel='Time (t)', ylabel='Output y(t)', title='Frequency Effect')
    ax.legend()
    plt.savefig('figures/frequency_effect.png', dpi=300)
    plt.close()

def plotKernelWidthEffect():
    T_values = [0.5, 1.0, 1.33]
    fig, ax = plt.subplots()
    for T_val in T_values:
        ax.plot(t, convResult(t, A, omega, phi, T_val), label=f'T = {T_val}')
    ax.set(xlabel='Time (t)', ylabel='Output y(t)', title='Kernel Width Effect')
    ax.legend()
    plt.savefig('figures/kernel_width_effect.png', dpi=300)
    plt.close()

def plotInputKernelOutput():
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 7), sharex=True)
    ax1.plot(t, inputSignal(t, A, omega, phi))
    ax1.set(ylabel='f(t)', title='Input Signal')
    ax2.plot(t, rectKernel(t, T))
    ax2.set(ylabel='h(t)', title='Rectangular Kernel')
    ax3.plot(t, convResult(t, A, omega, phi, T))
    ax3.set(xlabel='Time (t)', ylabel='y(t)', title='Convolution Result')
    plt.savefig('figures/input_kernel_output.png', dpi=300)
    plt.close()

def plotSpecialCases():
    fig, ax = plt.subplots()
    ax.plot(t, inputSignal(t, A, omega, phi), 'k--', label='Input')
    ax.plot(t, convResult(t, A, omega, phi, np.pi/omega), label='Null (ωT=π)')
    ax.plot(t, convResult(t, A, omega, phi, np.pi/(2*omega)), label='Max (ωT=π/2)')
    ax.set(xlabel='Time (t)', ylabel='Output', title='Special Cases')
    ax.legend()
    plt.savefig('figures/special_cases.png', dpi=300)
    plt.close()

def plotFrequencyResponse():
    omega_range = np.linspace(0.01, 10, 1000)
    fig, ax = plt.subplots()
    for T_val in [0.5, 1.0, 2.0]:
        H = 2 * np.sin(omega_range * T_val) / omega_range
        H[0] = 2 * T_val
        ax.plot(omega_range, H, label=f'T={T_val}')
    ax.set(xlabel='Frequency ω', ylabel='Gain', title='Frequency Response')
    ax.legend()
    plt.savefig('figures/frequency_response.png', dpi=300)
    plt.close()

plotAmplitudeEffect()
plotFrequencyEffect()
plotKernelWidthEffect()
plotInputKernelOutput()
plotSpecialCases()
plotFrequencyResponse()
