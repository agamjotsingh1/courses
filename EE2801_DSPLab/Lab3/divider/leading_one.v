// returns the position of leading 1
module leading_one #(
    parameter BITWIDTH = 32,
    parameter OUT_BITWIDTH = $clog2(BITWIDTH)
) (
    input wire [BITWIDTH-1:0] in,
    output reg [OUT_BITWIDTH-1:0] out
);
    reg found;

    always @(*) begin
        found = 1'b0;

        for(integer i = BITWIDTH-1; i >= 0; i = i - 1) begin
            if(in[i] == 1'b1 && found == 1'b0) begin
                out = i;
                found = 1'b1;
            end
        end
    end
endmodule