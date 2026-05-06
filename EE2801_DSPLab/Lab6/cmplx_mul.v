module cmplx_mul #(
    parameter INT_NBITS,
    parameter FRAC_NBITS
) (
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] num1,
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] num2,
    output wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out
);
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;
    
    wire [TOTAL_NBITS-1:0] re1, im1, re2, im2;
    wire [2*TOTAL_NBITS-1:0] p_re1_re2, p_im1_im2, p_re1_im2, p_im1_re2;
    wire [2*TOTAL_NBITS-1:0] big_out_re, big_out_im;

    assign {re1, im1} = num1;
    assign {re2, im2} = num2;

    assign p_re1_re2 = $signed(re1) * $signed(re2);
    assign p_im1_im2 = $signed(im1) * $signed(im2);
    assign p_re1_im2 = $signed(re1) * $signed(im2);
    assign p_im1_re2 = $signed(im1) * $signed(re2);

    assign big_out_re = p_re1_re2 - p_im1_im2;
    assign big_out_im = p_re1_im2 + p_im1_re2;

    assign out = {
        big_out_re[TOTAL_NBITS + FRAC_NBITS - 1 : FRAC_NBITS],
        big_out_im[TOTAL_NBITS + FRAC_NBITS - 1 : FRAC_NBITS]
    };

endmodule