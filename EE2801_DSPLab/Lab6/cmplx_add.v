module cmplx_add #(
    parameter INT_NBITS,
    parameter FRAC_NBITS
) (
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] num1,
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] num2,
    output wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out
);
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;
    
    wire [TOTAL_NBITS-1:0] re1, im1, re2, im2;
    wire [TOTAL_NBITS-1:0] a_re1_re2, a_im1_im2;

    assign {re1, im1} = num1;
    assign {re2, im2} = num2;

    assign a_re1_re2 = re1 + re2;
    assign a_im1_im2 = im1 + im2;

    assign out = {a_re1_re2, a_im1_im2};

endmodule