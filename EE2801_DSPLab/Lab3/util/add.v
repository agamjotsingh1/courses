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