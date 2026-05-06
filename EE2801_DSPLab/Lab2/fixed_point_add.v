module fixed_point_add #(
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
    localparam INT_PAD1  = (INT_NBITS  > INT_NBITS1)  ? (INT_NBITS  - INT_NBITS1)  : 0;
    localparam FRAC_PAD1 = (FRAC_NBITS > FRAC_NBITS1) ? (FRAC_NBITS - FRAC_NBITS1) : 0;
    localparam INT_PAD2  = (INT_NBITS  > INT_NBITS2)  ? (INT_NBITS  - INT_NBITS2)  : 0;
    localparam FRAC_PAD2 = (FRAC_NBITS > FRAC_NBITS2) ? (FRAC_NBITS - FRAC_NBITS2) : 0;

    wire [(INT_NBITS + FRAC_NBITS - 1):0] num1_padded, num2_padded;

    assign num1_padded = {{INT_PAD1{num1[INT_NBITS1 + FRAC_NBITS1 - 1]}}, num1, {FRAC_PAD1{1'b0}}};
    assign num2_padded = {{INT_PAD2{num2[INT_NBITS2 + FRAC_NBITS2 - 1]}}, num2, {FRAC_PAD2{1'b0}}};

    add #(
        .LEN(INT_NBITS + FRAC_NBITS)
    ) add_instance (
        .in1(num1_padded),
        .in2(num2_padded),
        .out(out)
    );
endmodule

module add #(
    parameter LEN
) (
    input wire [LEN-1:0] in1,
    input wire [LEN-1:0] in2,
    output reg [LEN-1:0] out
);
    reg [LEN-1:-1] cout;

    always @(*) begin
        cout[-1] = 1'b0;
        for(integer i = 0; i < LEN; i = i + 1) begin
            out[i] = in1[i] ^ in2[i] ^ cout[i - 1];
            cout[i] = (in1[i] & in2[i]) | (in1[i] & cout[i - 1]) | (in2[i] & cout[i - 1]);
        end
    end
endmodule