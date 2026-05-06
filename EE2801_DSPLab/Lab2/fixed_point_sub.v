module fixed_point_sub #(
    parameter INT_NBITS1,
    parameter FRAC_NBITS1,
    parameter INT_NBITS2,
    parameter FRAC_NBITS2,

    // max of integer and fractional parts respectively
    parameter INT_NBITS = INT_NBITS1 > INT_NBITS2 ? INT_NBITS1: INT_NBITS2,
    parameter FRAC_NBITS = FRAC_NBITS1 > FRAC_NBITS2 ? FRAC_NBITS1: FRAC_NBITS2
) (
    input wire [(INT_NBITS1 + FRAC_NBITS1 - 1):0] num1,
    input wire [(INT_NBITS2 + FRAC_NBITS2 - 1):0] num2,
    output wire [(INT_NBITS + FRAC_NBITS - 1):0] out
);
    fixed_point_add #(
        .INT_NBITS1(INT_NBITS1),
        .FRAC_NBITS1(FRAC_NBITS1),
        .INT_NBITS2(INT_NBITS2),
        .FRAC_NBITS2(FRAC_NBITS2)
    ) fixed_point_twos_complement_add (
        .num1(num1),
        .num2((~num2) + 1'b1),
        .out(out)
    );
endmodule