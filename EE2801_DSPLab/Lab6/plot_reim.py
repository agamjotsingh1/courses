import numpy as np
import matplotlib.pyplot as plt
import os
import tomllib

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

N = config["N"]
INT_NBITS = config["INT_NBITS"]
FRAC_NBITS = config["FRAC_NBITS"]
TOTAL_NBITS = INT_NBITS + FRAC_NBITS

SCALE = float(1 << FRAC_NBITS) 
MASK = (1 << TOTAL_NBITS) - 1 
SIGN_BIT = 1 << (TOTAL_NBITS - 1)    
SUB_VAL = 1 << TOTAL_NBITS       

SIG_NAMES = ["DC", "Nyquist", "Single Sine", "Fast Cosine", "Impulse"]

def parse_hex_to_complex(hex_str):
    hex_str = hex_str.strip()
    if not hex_str:
        return 0j
    
    full_val = int(hex_str, 16)
    
    imag_int = full_val & MASK
    real_int = (full_val >> TOTAL_NBITS) & MASK
    
    if real_int >= SIGN_BIT: 
        real_int -= SUB_VAL
    if imag_int >= SIGN_BIT: 
        imag_int -= SUB_VAL
        
    return complex(real_int / SCALE, imag_int / SCALE)

j = np.arange(N)
ideal_signals = [
    np.array([0.05] * N),
    np.array([0.05 * (1 if k % 2 == 0 else -1) for k in j]),
    np.array([0.05 * np.sin(2 * np.pi * k / N) for k in j]),
    np.array([0.05 * np.cos(4 * np.pi * k / N) for k in j]),
    np.array([0.05 if k == 0 else 0.0 for k in j])
]

for idx in range(1, 6):
    file_name = f"out_sig{idx}.hex"
    
    if not os.path.exists(file_name):
        print(f"Warning: {file_name} not found. Skipping plot for Signal {idx}.")
        continue

    hw_fft = np.zeros(N, dtype=complex)
    with open(file_name, "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines[:N]):
            hw_fft[i] = parse_hex_to_complex(line)

    ideal_time_sig = ideal_signals[idx - 1]
    ideal_fft = np.fft.fft(ideal_time_sig)

    real_ideal = np.real(ideal_fft)
    real_hw = np.real(hw_fft)
    
    imag_ideal = np.imag(ideal_fft)
    imag_hw = np.imag(hw_fft)

    real_error = np.abs(real_ideal - real_hw)
    imag_error = np.abs(imag_ideal - imag_hw)

    bins = np.arange(N)
    fig, axs = plt.subplots(3, 2, figsize=(12, 10))
    fig.suptitle(f"Signal {idx}: {SIG_NAMES[idx-1]} - Actual vs. Hardware (Q{INT_NBITS}.{FRAC_NBITS})", fontsize=16)

    axs[0, 0].stem(bins, real_ideal, basefmt="b-", linefmt="b-", markerfmt="bo")
    axs[0, 0].set_title("Ideal Real")
    axs[0, 0].set_ylabel("Real Part")
    axs[0, 0].grid(True)

    axs[0, 1].stem(bins, real_hw, basefmt="r-", linefmt="r-", markerfmt="ro")
    axs[0, 1].set_title(f"Hardware Real")
    axs[0, 1].grid(True)

    axs[1, 0].stem(bins, imag_ideal, basefmt="b-", linefmt="b-", markerfmt="bo")
    axs[1, 0].set_title("Ideal Imaginary")
    axs[1, 0].set_ylabel("Imaginary Part")
    axs[1, 0].grid(True)

    axs[1, 1].stem(bins, imag_hw, basefmt="r-", linefmt="r-", markerfmt="ro")
    axs[1, 1].set_title("Hardware Imaginary")
    axs[1, 1].grid(True)

    axs[2, 0].stem(bins, real_error, basefmt="k-", linefmt="k-", markerfmt="ko")
    axs[2, 0].set_title("Real Error (|Ideal - HW|)")
    axs[2, 0].set_xlabel("Frequency Bin")
    axs[2, 0].set_ylabel("Absolute Error")
    axs[2, 0].grid(True)

    axs[2, 1].stem(bins, imag_error, basefmt="k-", linefmt="k-", markerfmt="ko")
    axs[2, 1].set_title("Imaginary Error (|Ideal - HW|)")
    axs[2, 1].set_xlabel("Frequency Bin")
    axs[2, 1].grid(True)

    plt.tight_layout()
    plt.subplots_adjust(top=0.92)
    plt.savefig(f"fft_comparison_sig{idx}.png")
    print(f"Saved plot: fft_comparison_sig{idx}.png")

print(f"\nCompleted plotting using dynamically parsed Q({INT_NBITS}.{FRAC_NBITS}) format.")
plt.show()