import os
import numpy as np

def float_to_q2_14(val):
    scaled = round(val * (1 << 14))
    scaled = max(-(1 << 15), min((1 << 15) - 1, scaled))

    # convert to two's complement
    if scaled < 0:
        scaled += (1 << 16)

    return f"{scaled:04x}"

def generate_mif(filename, freq, fs, depth):
    t = np.arange(depth) / fs
    signal = 0.8*np.sin(2 * np.pi * freq * t)
    q_signal = [float_to_q2_14(s) for s in signal]
    
    with open(filename, 'w') as f:
        f.write(f"WIDTH=16;\n")
        f.write(f"DEPTH={depth};\n")
        f.write("ADDRESS_RADIX=UNS;\n")
        f.write("DATA_RADIX=HEX;\n")
        f.write("CONTENT BEGIN\n")
        
        for i, val in enumerate(q_signal):
            f.write(f"\t{i}: {val};\n")
            
        f.write("END;\n")

def main():
    output_dir = 'data'
    os.makedirs(output_dir, exist_ok=True)
    
    fs = 100000
    depth = 10000
    frequencies = [900, 1100, 2000]
    
    for freq in frequencies:
        filepath = os.path.join(output_dir, f"signal_{freq}.mif")
        generate_mif(filepath, freq, fs, depth)
        print(f"Generated: {filepath}")

if __name__ == "__main__":
    main()