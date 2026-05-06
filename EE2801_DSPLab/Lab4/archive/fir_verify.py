import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

TOTAL_NBITS = 16
frac_nbits = 14
MASK = (1 << TOTAL_NBITS) - 1

def hex_to_q2_14(hex_str):
    val = int(hex_str.strip(), 16)
    if val >= (1 << 15):
        val -= (1 << 16)
    return val / (1 << 14)

def load_hex_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return np.array([hex_to_q2_14(line) for line in lines if line.strip()])

def load_hex_file_int(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return np.array([int(line.strip(), 16) for line in lines if line.strip()])

def fixed_int_to_float(val_int):
    if val_int & (1 << (TOTAL_NBITS - 1)):
        val_int = val_int - (1 << TOTAL_NBITS)
    return float(val_int) / (2**frac_nbits)

def fp_mul(num1, num2):
    num1, num2 = int(num1), int(num2)
    is_neg1 = (num1 >> (TOTAL_NBITS - 1)) & 1
    is_neg2 = (num2 >> (TOTAL_NBITS - 1)) & 1
    
    abs_num1 = ((~num1) + 1) & MASK if is_neg1 else num1
    abs_num2 = ((~num2) + 1) & MASK if is_neg2 else num2
    
    res = 0
    for i in range(TOTAL_NBITS):
        if (abs_num2 >> i) & 1:
            res += (abs_num1 << i)
            
    if is_neg1 ^ is_neg2:
        if res != 0:
            res = (1 << (TOTAL_NBITS << 1)) - res
            
    return (res >> frac_nbits) & MASK

def fp_add(num1, num2):
    return (int(num1) + int(num2)) & MASK

def hardware_fir_direct(sig_int, coeffs_int):
    out = []
    x_ram = [0] * len(coeffs_int)
    for s in sig_int:
        x_ram = [int(s)] + x_ram[:-1]
        accum = 0
        for i in range(len(coeffs_int)):
            prod = fp_mul(x_ram[i], coeffs_int[i])
            accum = fp_add(accum, prod)
        out.append(accum)
    return out

def hardware_fir_symmetric(sig_int, coeffs_int):
    out = []
    num_taps = len(coeffs_int)
    x_ram = [0] * num_taps
    for s in sig_int:
        x_ram = [int(s)] + x_ram[:-1]
        accum = 0
        for i in range(num_taps // 2):
            pre_add = fp_add(x_ram[i], x_ram[num_taps - 1 - i])
            prod = fp_mul(pre_add, coeffs_int[i])
            accum = fp_add(accum, prod)
        out.append(accum)
    return out

def hardware_fir_genvar(sig_int, coeffs_int):
    out = []
    num_taps = len(coeffs_int)
    x_ram = [0] * num_taps
    for s in sig_int:
        x_ram = [int(s)] + x_ram[:-1]
        mult_out = [0] * num_taps
        for i in range(num_taps):
            mult_out[i] = fp_mul(x_ram[i], coeffs_int[i])
        
        add_out = mult_out[0]
        for i in range(1, num_taps):
            add_out = fp_add(add_out, mult_out[i])
        out.append(add_out)
    return out

def main():
    fs = 10000
    t = np.arange(0, 0.1, 1/fs)
    freqs = [950, 1100, 2000]
    
    quantized_coeffs = load_hex_file('coeffs.hex')
    if len(quantized_coeffs) == 0:
        print("coeffs.hex not found, please run fir_generate.py first.")
        return

    coeffs_int = load_hex_file_int('coeffs.hex')
        
    for i, f_sig in enumerate(freqs):
        print(f"\nComparing results for {f_sig}Hz signal:")
        
        sig = load_hex_file(f'sig{i+1}.hex')
        sig_int = load_hex_file_int(f'sig{i+1}.hex')
        
        # Golden standard float logic
        py_out = signal.lfilter(quantized_coeffs, 1.0, sig)
        
        # Load Verilog outputs
        dir_out = load_hex_file(f'out_direct_sig{i+1}.hex')
        sym_out = load_hex_file(f'out_sym_sig{i+1}.hex')
        gen_out = load_hex_file(f'out_gen_sig{i+1}.hex')

        # Load Verilog outputs as ints
        dir_out_int = load_hex_file_int(f'out_direct_sig{i+1}.hex')
        sym_out_int = load_hex_file_int(f'out_sym_sig{i+1}.hex')
        gen_out_int = load_hex_file_int(f'out_gen_sig{i+1}.hex')

        # Run hardware models in python
        py_hw_dir_int = hardware_fir_direct(sig_int, coeffs_int)
        py_hw_sym_int = hardware_fir_symmetric(sig_int, coeffs_int)
        py_hw_gen_int = hardware_fir_genvar(sig_int, coeffs_int)

        # Truncate testing scope because genvar simulation only ran for 200 samples
        lengths = [len(py_out), len(dir_out), len(sym_out), len(gen_out)]
        lengths = [l for l in lengths if l > 0]

        if not lengths:
            continue

        min_len = min(min(lengths), len(t))
        
        # Errors logic mimicking old_verify
        # Check first 10 computed stable values
        start_check = min_len // 2
        
        py_hw_dir = np.array([fixed_int_to_float(v) for v in py_hw_dir_int])
        py_hw_sym = np.array([fixed_int_to_float(v) for v in py_hw_sym_int])
        py_hw_gen = np.array([fixed_int_to_float(v) for v in py_hw_gen_int])

        print("\n--- Direct Check ---")
        err_hw_vs_vlog_dir = np.mean(np.abs(py_hw_dir[:min_len] - dir_out[:min_len]))
        err_hw_vs_lfilt_dir = np.mean(np.abs(py_hw_dir[:min_len] - py_out[:min_len]))
        print(f"Mean Abs Error(Verilog vs PyHW): {err_hw_vs_vlog_dir:.7f}")
        print(f"Mean Abs Error(PyHW vs lfilter): {err_hw_vs_lfilt_dir:.7f}")

        print("\n--- Symmetric Check ---")
        err_hw_vs_vlog_sym = np.mean(np.abs(py_hw_sym[:min_len] - sym_out[:min_len]))
        err_hw_vs_lfilt_sym = np.mean(np.abs(py_hw_sym[:min_len] - py_out[:min_len]))
        print(f"Mean Abs Error(Verilog vs PyHW): {err_hw_vs_vlog_sym:.7f}")
        print(f"Mean Abs Error(PyHW vs lfilter): {err_hw_vs_lfilt_sym:.7f}")

        print("\n--- Genvar Check ---")
        err_hw_vs_vlog_gen = np.mean(np.abs(py_hw_gen[:min_len] - gen_out[:min_len]))
        err_hw_vs_lfilt_gen = np.mean(np.abs(py_hw_gen[:min_len] - py_out[:min_len]))
        print(f"Mean Abs Error(Verilog vs PyHW): {err_hw_vs_vlog_gen:.7f}")
        print(f"Mean Abs Error(PyHW vs lfilter): {err_hw_vs_lfilt_gen:.7f}")

        # Plotting (Optional visual check)

        # Figure 1: Python lfilter vs Verilog
        fig1, axes1 = plt.subplots(2, 1, figsize=(10, 8))
        if len(py_out) > 0:
            axes1[0].plot(t[:min_len], py_out[:min_len], label='Python lfilter', linewidth=3, alpha=0.5)
        if len(dir_out) > 0:
            axes1[0].plot(t[:min_len], dir_out[:min_len], label='Verilog Direct', linestyle='--')
        if len(sym_out) > 0:
            axes1[0].plot(t[:min_len], sym_out[:min_len], label='Verilog Symmetric', linestyle=':')
        if len(gen_out) > 0:
            axes1[0].plot(t[:min_len], gen_out[:min_len], label='Verilog Genvar', linestyle='-.')
            
        axes1[0].set_title(f'lfilter vs Verilog (Signal {f_sig}Hz)')
        axes1[0].set_ylabel('Amplitude')
        axes1[0].legend(loc='upper right')
        axes1[0].grid(True)
        
        if len(dir_out) > 0:
            axes1[1].plot(t[:min_len], np.abs(py_out[:min_len] - dir_out[:min_len]), label='Error (Direct)')
        if len(sym_out) > 0:
            axes1[1].plot(t[:min_len], np.abs(py_out[:min_len] - sym_out[:min_len]), label='Error (Symmetric)')
        if len(gen_out) > 0:
            axes1[1].plot(t[:min_len], np.abs(py_out[:min_len] - gen_out[:min_len]), label='Error (Genvar)')
        axes1[1].set_title('Absolute Error: |lfilter - Verilog|')
        axes1[1].set_xlabel('Time (s)')
        axes1[1].set_ylabel('Error')
        axes1[1].legend(loc='upper right')
        axes1[1].grid(True)
        
        fig1.tight_layout()
        fig1.savefig(f'comparison_lfilter_sig{i+1}.png')
        plt.close(fig1)

        # Figure 2: Python HW vs Verilog
        fig2, axes2 = plt.subplots(2, 1, figsize=(10, 8))
        if len(dir_out) > 0:
            axes2[0].plot(t[:min_len], dir_out[:min_len], label='Verilog Direct', linewidth=3, alpha=0.4)
            axes2[0].plot(t[:min_len], py_hw_dir[:min_len], label='Python HW Direct', linestyle='--')
        if len(sym_out) > 0:
            axes2[0].plot(t[:min_len], sym_out[:min_len], label='Verilog Symmetric', linewidth=3, alpha=0.4)
            axes2[0].plot(t[:min_len], py_hw_sym[:min_len], label='Python HW Symmetric', linestyle='--')
        if len(gen_out) > 0:
            axes2[0].plot(t[:min_len], gen_out[:min_len], label='Verilog Genvar', linewidth=3, alpha=0.4)
            axes2[0].plot(t[:min_len], py_hw_gen[:min_len], label='Python HW Genvar', linestyle='--')
            
        axes2[0].set_title(f'Python HW vs Verilog (Signal {f_sig}Hz)')
        axes2[0].set_ylabel('Amplitude')
        axes2[0].legend(loc='upper right')
        axes2[0].grid(True)
        
        if len(dir_out) > 0:
            axes2[1].plot(t[:min_len], np.abs(py_hw_dir[:min_len] - dir_out[:min_len]), label='Error (Direct)')
        if len(sym_out) > 0:
            axes2[1].plot(t[:min_len], np.abs(py_hw_sym[:min_len] - sym_out[:min_len]), label='Error (Symmetric)')
        if len(gen_out) > 0:
            axes2[1].plot(t[:min_len], np.abs(py_hw_gen[:min_len] - gen_out[:min_len]), label='Error (Genvar)')
        axes2[1].set_title('Absolute Error: |Python HW - Verilog|')
        axes2[1].set_xlabel('Time (s)')
        axes2[1].set_ylabel('Error')
        axes2[1].legend(loc='upper right')
        axes2[1].grid(True)
        
        fig2.tight_layout()
        fig2.savefig(f'comparison_pyhw_sig{i+1}.png')
        plt.close(fig2)

if __name__ == "__main__":
    main()
