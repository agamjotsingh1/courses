module guess #(
    parameter LUT_SIZE = 64,
    parameter INT_NBITS = 16,
    parameter FRAC_NBITS = 16,
    parameter TOTAL_NBITS = INT_NBITS + FRAC_NBITS,
    parameter LEADING_ONE_NBITS = $clog2(TOTAL_NBITS)
) (
    input wire [TOTAL_NBITS-1:0] denom,
    output wire [TOTAL_NBITS-1:0] out
);
    localparam INDEX_NBITS = $clog2(LUT_SIZE);
    localparam INDEX_SHIFT_FACTOR = FRAC_NBITS - 1 - INDEX_NBITS;
    localparam SUB_CONST = 2**(FRAC_NBITS - 1);

    wire [LEADING_ONE_NBITS-1:0] leading_one_pos;

    leading_one #(
        .BITWIDTH(TOTAL_NBITS)
    ) leading_one_intstance (
        .in(denom),
        .out(leading_one_pos)
    );

    wire [TOTAL_NBITS-1:0] shifted_denom = 
        leading_one_pos < FRAC_NBITS - 1 ?
            (denom << (FRAC_NBITS - 1) - leading_one_pos):
            (denom >> leading_one_pos - (FRAC_NBITS - 1));

    wire [INDEX_NBITS-1:0] index = (shifted_denom - SUB_CONST) >> INDEX_SHIFT_FACTOR;

    wire [TOTAL_NBITS-1:0] lut_out;

    lut lut_instance (
        .index(index),
        .out(lut_out)
    );

    // denormalize the LUT output back
    assign out = leading_one_pos < (FRAC_NBITS - 1) ?
        (lut_out << ((FRAC_NBITS - 1) - leading_one_pos)):
        (lut_out >> (leading_one_pos - (FRAC_NBITS - 1)));
endmodule