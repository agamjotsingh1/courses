import math
import tomllib

# 1. Read the configuration file
with open("config.toml", "rb") as f:
    config = tomllib.load(f)

N = config["N"]
INT_NBITS = config["INT_NBITS"]
FRAC_NBITS = config["FRAC_NBITS"]
TOTAL_NBITS = INT_NBITS + FRAC_NBITS

# 2. Calculate dynamic scaling and formatting parameters
SCALE = 1 << FRAC_NBITS                  # Equivalent to 2^FRAC_NBITS
MASK = (1 << TOTAL_NBITS) - 1            # Creates a bitmask like 0xFF for 8 bits
HEX_DIGITS = (TOTAL_NBITS + 3) // 4      # Number of hex characters needed per number

def to_hex(real_val, imag_val=0):
    # Scale floating point to integer
    r = int(round(real_val * SCALE))
    i = int(round(imag_val * SCALE))
    
    # Apply bitmask for proper two's complement negative representation
    r_masked = r & MASK
    i_masked = i & MASK
    
    # Format dynamically: e.g., if HEX_DIGITS=2, format as "{:02x}"
    return f"{r_masked:0{HEX_DIGITS}x}{i_masked:0{HEX_DIGITS}x}"

# --- Generate the 5 test signals ---

# 1. DC Signal (Constant 0.5) -> Expect peak at bin 0
sig1 = [to_hex(0.05) for _ in range(N)]

# 2. Nyquist Frequency (Alternating 0.5, -0.5) -> Expect peak at bin N/2
sig2 = [to_hex(0.05 * (1 if j % 2 == 0 else -1)) for j in range(N)]

# 3. Single Sine Wave (1 cycle) -> Expect peaks at bin 1 and N-1
sig3 = [to_hex(0.05 * math.sin(2 * math.pi * j / N)) for j in range(N)]

# 4. Fast Cosine Wave (2 cycles) -> Expect peaks at bin 2 and N-2
sig4 = [to_hex(0.05 * math.cos(4 * math.pi * j / N)) for j in range(N)]

# 5. Impulse (0.5 at index 0, rest 0) -> Expect flat response across all bins
sig5 = [to_hex(0.05 if j == 0 else 0.0) for j in range(N)]

# --- Write to files ---
for idx, sig in enumerate([sig1, sig2, sig3, sig4, sig5], start=1):
    with open(f"sig{idx}.hex", "w") as f:
        for val in sig:
            f.write(val + "\n")
            
print(f"Generated 5 signal files successfully using Q({INT_NBITS}.{FRAC_NBITS}) format.")
print(f"Total width per word: {2 * TOTAL_NBITS} bits ({HEX_DIGITS * 2} hex characters).")