// Newton Raphson iteration
module newton_raphson #(
    parameter INT_NBITS,
    parameter FRAC_NBITS
) (
    input wire [(INT_NBITS + FRAC_NBITS - 1):0] current,
    input wire [(INT_NBITS + FRAC_NBITS - 1):0] denom,
    output wire [(INT_NBITS + FRAC_NBITS - 1):0] out
);
    localparam TWO = {{(INT_NBITS + FRAC_NBITS - 1){1'b0}}, 1'b1} << (FRAC_NBITS + 1);

    wire [(INT_NBITS + FRAC_NBITS - 1):0] x_d, two_minus_x_d;

    fp_mul #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) fp_mul_instance1 (
        .num1(current), 
        .num2(denom),
        .out(x_d)
    );

    fp_sub #(
        .INT_NBITS1(INT_NBITS),
        .FRAC_NBITS1(FRAC_NBITS),
        .INT_NBITS2(INT_NBITS),
        .FRAC_NBITS2(FRAC_NBITS)
    ) fp_sub_instance1 (
        .num1(TWO), 
        .num2(x_d),
        .out(two_minus_x_d)
    );

    fp_mul #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) fp_mul_instance2 (
        .num1(current), 
        .num2(two_minus_x_d),
        .out(out)
    );
endmodule