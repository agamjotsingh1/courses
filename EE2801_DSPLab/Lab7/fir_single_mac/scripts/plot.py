import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- Configuration ---
freq = 2000
csv_file = os.path.join('output_files', f'output.csv')
sampling_freq = 100000  # 100 kHz
fraction_bits = 14

# --- Parse Quartus CSV ---
skip_rows = 0
with open(csv_file, 'r') as f:
    for i, line in enumerate(f):
        if line.startswith("time unit: ns") or line.startswith("Data Index"):
            skip_rows = i
            break

df = pd.read_csv(csv_file, skiprows=skip_rows)
df.columns = df.columns.str.strip()

col_in = [c for c in df.columns if 'input_signal' in c][0]
col_out = [c for c in df.columns if 'output_signal' in c][0]

# --- STRICT BASE-10 DECIMAL PARSER ---
# Safely handles Quartus 'X' states by dropping them
in_data = pd.to_numeric(df[col_in], errors='coerce').dropna()
out_data = pd.to_numeric(df[col_out], errors='coerce').dropna()

# Reverse Q2.14 Quantization
in_float = in_data / (2**fraction_bits)
out_float = out_data / (2**fraction_bits)

# --- Create the Time Axis ---
num_samples = len(in_float)
time_ms = (np.arange(num_samples) / sampling_freq) * 1000

# --- Visualization ---
plt.figure(figsize=(14, 6))

plt.plot(time_ms, in_float.values, label="Actual Output")
plt.plot(time_ms, out_float.values, label="FPGA Output", linestyle='--')

plt.title(f"FIR Low-Pass Filter FPGA Plot {freq}Hz")
plt.xlabel("Time (ms)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend(fontsize=9)
plt.tight_layout()

png_file = os.path.join('data', f'out_sig{freq}.png')
plt.savefig(png_file)

# Scope to the first 5 milliseconds
# plt.xlim(0, 10.0) 

plt.show()