import csv
import numpy as np
import matplotlib.pyplot as plt

f_s = 48e3 # sampling frequency
f = 1e3

plot_cycles = 5
plot_ticks = int((plot_cycles/f)/(1/f_s))

formats = [(2, 14), (4, 12), (8, 4)]

for index, format in enumerate(formats):
    integer_bits, fraction_bits = format;
    t = []
    x_t = []
    quantized_x_t = []
    error = []

    with open(f"data/q{integer_bits}_{fraction_bits}.csv", mode ='r') as file:
        data = csv.reader(file)
        next(data) # skip header

        for lines in data:
            t.append(float(lines[0]))
            x_t.append(float(lines[1]))
            quantized_x_t.append(float(lines[2]))
            error.append(float(lines[3]))

    t = np.array(t)
    x_t = np.array(x_t)
    quantized_x_t = np.array(quantized_x_t)
    error = np.array(error)

    plt.step(t[:plot_ticks], x_t[:plot_ticks], label=f"Original Signal $x(t)$")
    plt.step(t[:plot_ticks], quantized_x_t[:plot_ticks], label=f"Quantized signal $x(t)$")
    plt.title(f"<Verilog> Quantized vs Original plots with Q{format}")
    plt.legend()
    plt.savefig(f"plots/verilog_q{integer_bits}_{fraction_bits}")
    plt.show()

    plt.step(t[:plot_ticks], error[:plot_ticks], label="Quantization error")
    plt.title(f"<Verilog> Quantization error with Q{format}")
    plt.legend()
    plt.savefig(f"plots/verilogerror_q{integer_bits}_{fraction_bits}")
    plt.show()

    sqnr = np.mean(x_t**2)/np.mean(error**2)
    print(f"Q{format} -> SQNR = {sqnr}")