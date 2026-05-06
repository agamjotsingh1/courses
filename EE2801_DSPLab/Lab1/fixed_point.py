import numpy as np
import matplotlib.pyplot as plt

# x(t) = 2sin(2*pi*f*t)
f_s = 48e3 # sampling frequency
f = 1e3

time_duration = 1
plot_cycles = 5
plot_ticks = int((plot_cycles/f)/(1/f_s))

# formats in Q(_, _) notation
formats = [(2, 14), (4, 12), (8, 4)]

# time array
t = np.arange(0, time_duration, 1/f_s)
x_t = 2*np.sin(2*np.pi*f*t)

for index, format in enumerate(formats):
    integer_bits, fraction_bits = format;

    # clip the data to avoid overflow
    max_val = (2**(integer_bits + fraction_bits - 1) - 1)/(2**fraction_bits)
    min_val = (-2**(integer_bits + fraction_bits - 1))/(2**fraction_bits)
    clipped_x_t = np.clip(x_t, min_val, max_val)

    # quantize x(t) by using round
    quantized_x_t = np.round(clipped_x_t * (2**fraction_bits)) / (2**fraction_bits)

    # plot only 'plot_cycles' of original vs quantized signal
    plt.step(t[:plot_ticks], x_t[:plot_ticks], label=f"Original Signal $x(t)$")
    plt.step(t[:plot_ticks], quantized_x_t[:plot_ticks], label=f"Quantized signal $x(t)$")
    plt.title(f"Quantized vs Original plots with Q{format}")
    plt.legend()
    plt.savefig(f"plots/python_q{integer_bits}_{fraction_bits}")
    plt.show()

    error = (x_t - quantized_x_t)

    # plot the errors with respect to time (for 'plot_cycles')
    plt.step(t[:plot_ticks], error[:plot_ticks], label="Quantization error")
    plt.title(f"Quantization error with Q{format}")
    plt.legend()
    plt.savefig(f"plots/pythonerror_q{integer_bits}_{fraction_bits}")
    plt.show()

    # print the sqnr
    sqnr = np.mean(x_t**2)/np.mean(error**2)
    print(f"Q{format} -> SQNR = {sqnr}")
