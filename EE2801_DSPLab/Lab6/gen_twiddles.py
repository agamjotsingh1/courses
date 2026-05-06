import math
import tomllib

def float_to_fixed(val, frac_nbits, total_nbits):
    fixed_val = round(val * (1 << frac_nbits))
    return fixed_val & ((1 << total_nbits) - 1)

with open("config.toml", "rb") as f:
    config = tomllib.load(f)

n = config["N"]
int_nbits = config["INT_NBITS"]
frac_nbits = config["FRAC_NBITS"]

total_nbits = int_nbits + frac_nbits
out_width = 2 * total_nbits

exp_max = (n // 2) - 1
exp_bits = max(1, math.ceil(math.log2(exp_max + 1)))

with open("twiddles_lut.v", "w") as f:
    f.write("//AUTO-GENERATED FILE DO NOT EDIT!\n")
    f.write("module twiddles_lut #(\n")
    f.write(f"    parameter N = {n},\n")
    f.write(f"    parameter INT_NBITS = {int_nbits},\n")
    f.write(f"    parameter FRAC_NBITS = {frac_nbits}\n")
    f.write(") (\n")
    f.write(f"    input wire [{exp_bits - 1}:0] exp,\n")
    f.write(f"    output reg [{out_width - 1}:0] out\n")
    f.write(");\n\n")

    f.write("    always @(*) begin\n")
    f.write("        case (exp)\n")

    for k in range(n // 2):
        angle = -2.0 * math.pi * k / n
        real_part = math.cos(angle)
        imag_part = math.sin(angle)

        real_fixed = float_to_fixed(real_part, frac_nbits, total_nbits)
        imag_fixed = float_to_fixed(imag_part, frac_nbits, total_nbits)

        combined = (real_fixed << total_nbits) | imag_fixed
        hex_chars = (out_width + 3) // 4

        f.write(f"            {exp_bits}'d{k}: out = {out_width}'h{combined:0{hex_chars}X};\n")

    f.write(f"            default: out = {out_width}'h0;\n")
    f.write("        endcase\n")
    f.write("    end\n\n")
    f.write("endmodule\n")