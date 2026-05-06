import tomllib
import csv
import numpy as np

def hex_to_float(hex_str):
    val_int = int(hex_str, 16)
    return float(val_int) / (2**frac_nbits)

def float_to_fixed(num):
    return float(np.round(num * (2**frac_nbits)))/2**frac_nbits

with open("config.toml", "rb") as file:
    config = tomllib.load(file)

indexing = int(config['indexing'])
int_nbits = int(config["int_nbits"])
frac_nbits = int(config["frac_nbits"])
size = 2**indexing

TOTAL_NBITS = int_nbits + frac_nbits
MASK = (1 << TOTAL_NBITS) - 1

nr_iters = int(config["nr_iters"])

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

def fp_sub(num1, num2):
    return (num1 + ((~num2) + 1)) & MASK

def init_lut():
    lut_dict = {}
    sqrt3_minus_1_float = np.sqrt(3) - 1.0
    sqrt3_minus_1_fixed = int(np.round(sqrt3_minus_1_float * (1 << frac_nbits))) & MASK
    four_fixed = 4 << frac_nbits
    c_fixed = fp_mul(four_fixed, sqrt3_minus_1_fixed)
    two_fixed = 2 << frac_nbits
    
    for i in range(size):
        val_fixed = (1 << (frac_nbits - 1)) + (i << (frac_nbits - 1 - indexing))
        two_val_fixed = fp_mul(two_fixed, val_fixed)
        lut_out = fp_sub(c_fixed, two_val_fixed)
        lut_dict[i] = lut_out
        
    return lut_dict

LUT = init_lut()

def leading_one(in_val):
    found = 0
    out = 0
    for i in range(TOTAL_NBITS - 1, -1, -1):
        if ((int(in_val) >> i) & 1) == 1 and found == 0:
            out = i
            found = 1
    return out

def guess(denom_val):
    INDEX_SHIFT_FACTOR = frac_nbits - 1 - indexing
    SUB_CONST = 1 << (frac_nbits - 1)
    
    lo_pos = leading_one(denom_val)
    
    if lo_pos < (frac_nbits - 1):
        shifted_denom = (int(denom_val) << ((frac_nbits - 1) - lo_pos)) & MASK
    else:
        shifted_denom = (int(denom_val) >> (lo_pos - (frac_nbits - 1))) & MASK
        
    index = ((shifted_denom + ((~SUB_CONST) + 1)) & MASK) >> INDEX_SHIFT_FACTOR
    index = index & ((1 << indexing) - 1)
    
    lut_out = LUT[index]
    
    if lo_pos < (frac_nbits - 1):
        out = (lut_out << ((frac_nbits - 1) - lo_pos)) & MASK
    else:
        out = (lut_out >> (lo_pos - (frac_nbits - 1))) & MASK
        
    return out

def newton_raphson(current, denom_val):
    TWO = 1 << (frac_nbits + 1)
    x_d = fp_mul(current, denom_val)
    two_minus_x_d = fp_sub(TWO, x_d)
    out = fp_mul(current, two_minus_x_d)
    return out

def fp_inv(denom_val):
    current = guess(denom_val)
    for _ in range(nr_iters):
        current = newton_raphson(current, denom_val)
    return current

def fp_div(num1, num2):
    inv = fp_inv(num2)
    return fp_mul(num1, inv)

def div(num1, num2):
    return float_to_fixed(num1)/float_to_fixed(num2)

with open("testing/results.csv", mode="r") as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        num1_hex = row["num1"].strip()
        num2_hex = row["num2"].strip()
        verilog_div_hex = row["div"].strip()
        
        num1_int = int(num1_hex, 16)
        num2_int = int(num2_hex, 16)
        
        num1_float = fixed_int_to_float(num1_int)
        num2_float = fixed_int_to_float(num2_int)
        verilog_div = fixed_int_to_float(int(verilog_div_hex, 16))
        
        expected_div_int = fp_div(num1_int, num2_int)
        expected_div = fixed_int_to_float(expected_div_int)
        
        error = abs(expected_div - verilog_div)
        error_actual = abs(div(num1_float, num2_float) - verilog_div)

        print(f"TEST {num1_float:.3f}/{num2_float:.3f} > Verilog: {verilog_div:.7f}, Expected (actual): {expected_div:.7f}, Error (verilog vs python NR): {error:.7f}, Error (NR vs Actual): {error_actual:.7f}")