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

def q2_14_to_float(hex_str):
    val = int(hex_str, 16)

    if val >= (1 << 15):
        val -= (1 << 16)

    return val / (1 << 14)

def main():
    fs = 100000
    fc = 1000
    num_taps = 100
    
    coeffs = signal.firwin(num_taps, fc, fs=fs, window='hamming')

    with open('./data/coeffs.hex', 'w') as f:
        for c in coeffs:
            f.write(float_to_q2_14(c) + '\n')

    print("{" + ",\n".join(["16'h" + str(float_to_q2_14(c)) for c in coeffs]) + "}")
            
    t = np.arange(10000)/fs
    freqs = [950, 1100, 2000]
    signals = []
    
    for i, f_sig in enumerate(freqs):
        sig = 0.8 * np.sin(2 * np.pi * f_sig * t)
        signals.append(sig)
        
        filename = f'./data/sig{i+1}.hex'

        with open(filename, 'w') as f:
            for s in sig:
                f.write(float_to_q2_14(s) + '\n')

if __name__ == "__main__":
    main()
