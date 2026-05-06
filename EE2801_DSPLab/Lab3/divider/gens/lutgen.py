import tomllib
import numpy as np

# read the config
with open("config.toml", "rb") as file:
    config = tomllib.load(file)

indexing = int(config['indexing'])
int_nbits = int(config["int_nbits"])
frac_nbits = int(config["frac_nbits"])

# generates LUT verilog code for initial guess estimate
size = 2**indexing

def lut(i):
    val = 0.5 + (float(i/size))*0.5
    val = 4*(np.sqrt(3) - 1) - 2*val
    # val = (48/17) - (32/17)*val
    val = format(np.round(val * (2**frac_nbits)).astype(np.int64), f"{int_nbits + frac_nbits}b").strip()
    return val

with open("divider/lut.v", "w") as file:
    lines =\
f"""// AUTO-GENERATED FILE. DO NOT EDIT DIRECTLY.
// Sourced from lutgen.py
module lut (
    input wire [{indexing-1}:0] index,
    output reg [{int_nbits + frac_nbits - 1}:0] out
);
    always @(*) begin
        case(index)
"""

    for i in range(size):
        lines += f"\t\t\t{indexing}'b{format(i, f"{indexing}b").strip()}: out = {int_nbits + frac_nbits}'b{lut(i)};\n"

    lines +=\
f"""            default: out = {int_nbits + frac_nbits}'b0;
        endcase
    end
endmodule\n"""

    file.writelines(lines)

print("Successfully generated lut.v")