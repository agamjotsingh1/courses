import numpy as np
import matplotlib.pyplot as plt

# x(t) = 2sin(2*pi*f*t)
f_s = 48e3 # sampling frequency
f = 1e3

time_duration = 1

# formats in Q(_, _) notation
formats = [(3, 14), (5, 12)]

# time array
t = np.arange(0, time_duration, 1/f_s)
# x_t = 2*np.sin(2*np.pi*f*t)
x_t = np.array([0.5175, -0.5175])

for index, format in enumerate(formats):
    integer_bits, fraction_bits = format;

    # clip the data to avoid overflow
    max_val = (2**(integer_bits + fraction_bits - 1) - 1)/(2**fraction_bits)
    min_val = (-2**(integer_bits + fraction_bits - 1))/(2**fraction_bits)
    clipped_x_t = np.clip(x_t, min_val, max_val)

    # quantize x(t) by using round
    quantized_x_t = np.round(clipped_x_t * (2**fraction_bits)) / (2**fraction_bits)

    int_part = np.round(quantized_x_t)
    frac_part = quantized_x_t - int_part

    int_bin_part = [bin(a) for a in int_part.astype(int)]
    frac_bin_part = [bin(a) for a in np.round(frac_part * (2**fraction_bits)).astype(int)]

    print(quantized_x_t)
    print(int_part)
    print(int_bin_part)
    print(frac_part)
    print(frac_bin_part)

    # with open(f"data/.csv", mode ='r') as file:
    #     data = csv.reader(file)
    #     next(data) # skip header

    #     for lines in data:
    #         t.append(float(lines[0]))
    #         x_t.append(float(lines[1]))
    #         quantized_x_t.append(float(lines[2]))
    #         error.append(float(lines[3]))