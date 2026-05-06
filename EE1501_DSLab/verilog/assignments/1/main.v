module priority_encoder (
    input [3:0] in,
    output reg [1:0] out,
    output reg valid
);
    always @(*) begin
        valid = | in;
        casez (in)
            4'b1zzz: out = 2'b11;
            4'b01zz: out = 2'b10;
            4'b001z: out = 2'b01;
            4'b0001: out = 2'b00;
            default: out = 2'b00;
        endcase
    end
endmodule

module even_parity_generator(
    input [7:0] data,
    output parity
);
    assign parity = ^ data;
endmodule

module up_counter(
    input clk,
    input reset,
    input enable,
    output reg [3:0] count
);
    always @(posedge clk or posedge reset) begin
        if(reset) count <= 4'b0000;
        else if(enable) begin
            count[0] <= ~count[0];
            if(count[0]) count[1] <= ~count[1]; 
            if(count[0] & count[1]) count[2] <= ~count[2]; 
            if(count[0] & count[1] & count[2]) count[3] <= ~count[3]; 
        end
    end
endmodule
