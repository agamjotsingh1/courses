module rotate #(
    parameter N,
    parameter INT_NBITS,
    parameter FRAC_NBITS
) (
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] in,
    input wire [($clog2(N/2)-1) : 0] twiddle_exp, 
    output wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out
);
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;
    wire [2*(TOTAL_NBITS) - 1 : 0] twiddle;

    twiddles_lut #(
        .N(N),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) u_twiddles_lut (
        .exp(twiddle_exp),
        .out(twiddle)
    );

    cmplx_mul #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) u_cmplx_mul (
        .num1(in),
        .num2(twiddle),
        .out(out)
    );
endmodule