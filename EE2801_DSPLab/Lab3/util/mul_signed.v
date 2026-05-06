module mul_signed #(
    parameter LEN1,
    parameter LEN2,
    parameter LEN = LEN1 + LEN2
) (
    input wire [(LEN1 - 1):0] in1,
    input wire [(LEN2 - 1):0] in2,
    output reg [(LEN - 1):0] out
);
    reg [(LEN - 1):0] in1_extended, in2_extended;

    always @(*) begin
        in1_extended = {{(LEN - LEN1){in1[LEN1 - 1]}}, in1};
        in2_extended = {{(LEN - LEN2){in2[LEN2 - 1]}}, in2};
        out = 0;
        for(integer i = 0; i < LEN; i = i + 1) begin
            out = out + (in1_extended[i] ? in2_extended: {LEN{1'b0}});
            in2_extended = in2_extended << 1;
        end
    end
endmodule