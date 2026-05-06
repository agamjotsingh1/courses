module fp_div #(
    parameter INT_NBITS1,
    parameter FRAC_NBITS1,
    parameter INT_NBITS2,
    parameter FRAC_NBITS2,
    parameter NR_ITERS,
    parameter LUT_SIZE,

    // max of integer and fractional parts respectively
    parameter INT_NBITS = INT_NBITS1 > INT_NBITS2 ? INT_NBITS1: INT_NBITS2,
    parameter FRAC_NBITS = FRAC_NBITS1 > FRAC_NBITS2 ? FRAC_NBITS1: FRAC_NBITS2
) (
    input wire clk,
    input wire rst,
    input wire [(INT_NBITS1 + FRAC_NBITS1 - 1):0] num1,
    input wire [(INT_NBITS2 + FRAC_NBITS2 - 1):0] num2,

    output reg done,
    output reg [(INT_NBITS + FRAC_NBITS - 1):0] out
);
    localparam INT_PAD1  = (INT_NBITS  > INT_NBITS1)  ? (INT_NBITS  - INT_NBITS1)  : 0;
    localparam FRAC_PAD1 = (FRAC_NBITS > FRAC_NBITS1) ? (FRAC_NBITS - FRAC_NBITS1) : 0;
    localparam INT_PAD2  = (INT_NBITS  > INT_NBITS2)  ? (INT_NBITS  - INT_NBITS2)  : 0;
    localparam FRAC_PAD2 = (FRAC_NBITS > FRAC_NBITS2) ? (FRAC_NBITS - FRAC_NBITS2) : 0;

    wire [(INT_NBITS + FRAC_NBITS - 1):0] num1_padded, num2_padded;

    assign num1_padded = {{INT_PAD1{num1[INT_NBITS1 + FRAC_NBITS1 - 1]}}, num1, {FRAC_PAD1{1'b0}}};
    assign num2_padded = {{INT_PAD2{num2[INT_NBITS2 + FRAC_NBITS2 - 1]}}, num2, {FRAC_PAD2{1'b0}}};

    wire [(INT_NBITS + FRAC_NBITS - 1):0] num2_inv;

    reg inv_done;
    reg [(INT_NBITS + FRAC_NBITS - 1):0] mul_out;

    fp_inv #(
        .LUT_SIZE(LUT_SIZE),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS),
        .NR_ITERS(NR_ITERS)
    ) fp_inv_instance (
        .clk(clk),
        .rst(rst),
        .denom(num2_padded),
        .done(inv_done),
        .out(num2_inv)
    );

    fp_mul #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) fp_mul_instance1 (
        .num1(num1_padded), 
        .num2(num2_inv),
        .out(mul_out)
    );

    always @(posedge clk) begin
        if(rst) begin
            done <= 1'b0;
        end
        else if(inv_done & (~done)) begin
            out <= mul_out;
            done <= 1'b1;
        end
    end

endmodule