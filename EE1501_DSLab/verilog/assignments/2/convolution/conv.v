module conv(
    input [3:0] x[7:0],
    input [3:0] h[7:0],
    output reg [3:0] y[14:0]
);

    always @(*) begin
        for (integer i = 0; i < 15; i = i + 1) y[i] = 0;

        for(integer i = 0; i < 8; i = i + 1) begin
            for(integer j = 0; j < 8; j = j + 1) begin
                y[i + j] = y[i + j] + x[i]*h[j];
            end
        end
    end
endmodule
