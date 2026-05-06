module cmplx_sub #(
    parameter INT_NBITS,
    parameter FRAC_NBITS
) (
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] num1,
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] num2,
    output wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out
);
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;
    
    wire [TOTAL_NBITS-1:0] re1, im1, re2, im2;
    wire [TOTAL_NBITS-1:0] s_re1_re2, s_im1_im2;

    assign {re1, im1} = num1;
    assign {re2, im2} = num2;

    assign s_re1_re2 = re1 - re2;
    assign s_im1_im2 = im1 - im2;

    assign out = {s_re1_re2, s_im1_im2};

endmodule