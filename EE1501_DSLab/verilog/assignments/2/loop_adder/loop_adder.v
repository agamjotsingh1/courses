module loop_adder (
    input [7:0] a,
    input [7:0] b,
    input cin,
    output reg [7:0] sum,
    output reg cout
);
    always @(*) begin
        cout = cin;
        for (integer i = 0; i < 8; i = i + 1) begin
            sum[i] = a[i] ^ b[i] ^ cout;
            cout = (a[i] & b[i]) | (cout & a[i]) | (cout & b[i]);
        end
    end
endmodule
