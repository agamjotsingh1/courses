import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def float_to_q2_14(val):
    scaled = round(val * (1 << 14))
    scaled = max(-(1 << 15), min((1 << 15) - 1, scaled))

    # convert to two's complement
    if scaled < 0:
        scaled += (1 << 16)

    return f"{scaled:04x}"

def float_to_shifted_int_2_14(val):
    scaled = round(val * (1 << 14))
    scaled = max(-(1 << 15), min((1 << 15) - 1, scaled))

    return scaled

def q2_14_to_float(hex_str):
    val = int(hex_str, 16)

    if val >= (1 << 15):
        val -= (1 << 16)

    return val / (1 << 14)

def main():
    fs = 10000
    fc = 1000
    num_taps = 100
    
    coeffs = signal.firwin(num_taps, fc, fs=fs, window='hamming')

    with open('./data/coeffs.hex', 'w') as f:
        for c in coeffs:
            f.write(float_to_q2_14(c) + '\n')

    with open('./data/coeffs.txt', 'w') as f:
        for i, c in enumerate(coeffs):
            f.write(str(float_to_shifted_int_2_14(c)))
            if i < len(coeffs) - 1:
                f.write(" ,")
            
    t = np.arange(0, 0.1, 1/fs) # 0.1 secs = 1000 samples
    freqs = [950, 1100, 2000]
    signals = []
    
    for i, f_sig in enumerate(freqs):
        sig = 0.8 * np.sin(2 * np.pi * f_sig * t)
        signals.append(sig)
        
        filename = f'./data/sig{i+1}.hex'
        filename_ip = f'./data/sig{i+1}.txt'

        with open(filename, 'w') as f:
            for s in sig:
                f.write(float_to_q2_14(s) + '\n')

        with open(filename_ip, 'w') as f:
            for s in sig:
                f.write(str(float_to_shifted_int_2_14(s)))
                if i < len(coeffs) - 1:
                    f.write(" ,")


if __name__ == "__main__":
    main()
