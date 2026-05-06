module fp_mul #(
    parameter INT_NBITS,
    parameter FRAC_NBITS
) (
    input wire [(INT_NBITS + FRAC_NBITS - 1):0] num1,
    input wire [(INT_NBITS + FRAC_NBITS - 1):0] num2,
    output wire [(INT_NBITS + FRAC_NBITS - 1):0] out
);
    wire [(2*(INT_NBITS + FRAC_NBITS) - 1):0] big_out;

    mul_signed #(
        .LEN1(INT_NBITS + FRAC_NBITS),
        .LEN2(INT_NBITS + FRAC_NBITS)
    ) mul_signed_instance (
        .in1(num1),
        .in2(num2),
        .out(big_out)
    );

    assign out = big_out >> FRAC_NBITS;
endmodule