module butterfly #(
    parameter INT_NBITS = 8,
    parameter FRAC_NBITS = 8
) (
    input wire signed [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] a,
    input wire signed [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] b,
    input wire signed [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] w, 
    output wire signed [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out_top,
    output wire signed [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out_bot
);
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;
    wire signed [2*TOTAL_NBITS-1:0] wb; 

    cmplx_mul #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) u_cmplx_mul (
        .num1(w),
        .num2(b),
        .out(wb)
    );

    cmplx_add #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) u_cmplx_add (
        .num1(a),
        .num2(wb),
        .out(out_top)
    );

    cmplx_sub #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) u_cmplx_sub (
        .num1(a),
        .num2(wb),
        .out(out_bot)
    );
endmodule