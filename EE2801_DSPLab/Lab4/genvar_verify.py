import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter
from util import pyhw
from genvar import pyhw_genvar

def read_hex_file(filepath):
    with open(filepath, 'r') as f:
        return [int(line.strip(), 16) for line in f if line.strip()]

def to_signed_float(val_array):
    arr = np.array(val_array, dtype=np.int32)
    arr[arr >= (1 << (pyhw.TOTAL_NBITS - 1))] -= (1 << pyhw.TOTAL_NBITS)
    return arr / (1 << pyhw.FRAC_NBITS)

coeffs_raw = read_hex_file(os.path.join('data', 'coeffs.hex'))
coeffs_float = to_signed_float(coeffs_raw)
num_taps = len(coeffs_raw)

for i in range(1, 4):
    sig_raw = read_hex_file(os.path.join('data', f'sig{i}.hex'))
    verilog_raw = read_hex_file(os.path.join('data', f'out_genvar_sig{i}.hex'))
    
    sig_padded = sig_raw + [0] * (num_taps - 1)
    pyhw_out = pyhw_genvar.hw_fir_genvar(sig_padded, coeffs_raw)
    
    sig_float = to_signed_float(sig_padded)
    ideal_out = lfilter(coeffs_float, [1.0], sig_float)
    
    verilog_float = to_signed_float(verilog_raw)
    pyhw_float = to_signed_float(pyhw_out)
    
    min_len = min(len(verilog_float), len(pyhw_float), len(ideal_out))
    v_f = verilog_float[:min_len]
    p_f = pyhw_float[:min_len]
    i_f = ideal_out[:min_len]
    
    err_ideal = np.abs(v_f - i_f)
    err_hw = np.abs(v_f - p_f)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle(f'Signal {i} Analysis for Genvar')
    
    ax1.plot(v_f, label='Verilog RTL', alpha=0.9)
    ax1.plot(i_f, label='Ideal (lfilter)', linestyle='dashed', alpha=0.7)
    ax1.set_title('Filtering Output')
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(err_ideal, label='Quantization Error', color='red', alpha=0.7)
    ax2.plot(err_hw, label='Logic Error (RTL vs PyHW)', color='black', linestyle='dotted')
    ax2.set_title('Errors')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()

    plt.savefig(f"plots/genvar_sig{i}.png")
    plt.show()
