module butterfly #(
    parameter INT_NBITS,
    parameter FRAC_NBITS
) (
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] a,
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] b,
    output wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out_add,
    output wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out_sub
);
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;

    cmplx_add #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) u_cmplx_add (
        .num1(a),
        .num2(b),
        .out(out_add)
    );

    cmplx_sub #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) u_cmplx_sub (
        .num1(a),
        .num2(b),
        .out(out_sub)
    );
endmodule