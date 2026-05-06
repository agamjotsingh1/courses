import numpy as np
import tomllib

def float_to_fixed_hex(val, int_nbits, frac_nbits):
    total_bits = int_nbits + frac_nbits
    scaled = round(val * (1 << frac_nbits))
    
    max_val = (1 << (total_bits - 1)) - 1
    min_val = -(1 << (total_bits - 1))
    scaled = max(min_val, min(max_val, scaled))
    
    if scaled < 0:
        scaled += (1 << total_bits)
        
    hex_digits = (total_bits + 3) // 4
    return f"{scaled:0{hex_digits}x}"

def main():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
        
    n = config["N_sig"]
    int_bits = config["INT_NBITS"]
    frac_bits = config["FRAC_NBITS"]
    
    t = np.arange(n)
    freq = 2.0 
    sig_real = 0.5 * np.sin(2 * np.pi * freq * t / n)
    
    with open('sig.hex', 'w') as f:
        for s in sig_real:
            real_hex = float_to_fixed_hex(s, int_bits, frac_bits)
            imag_hex = float_to_fixed_hex(0.0, int_bits, frac_bits)
            f.write(real_hex + imag_hex + '\n')

if __name__ == "__main__":
    main()
