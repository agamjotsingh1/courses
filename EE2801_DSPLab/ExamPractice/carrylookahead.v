`timescale 1ns/1ps

module carrylookahead (
    input wire [3:0] in1,
    input wire [3:0] in2,
    input wire cin,
    output wire [3:0] out,
    output wire cout
);
    wire [3:0] p, g, c;

    assign p = in1 ^ in2;
    assign g = in1 & in2;

    assign c[0] = cin;
    assign c[1] = g[0] | (p[0] & cin);
    assign c[2] = g[1] | (p[1] & g[0]) | (p[1] & p[0] & cin);
    assign c[3] = g[2] | (p[2] & g[1]) | (p[2] & p[1] & g[0]) | (p[2] & p[1] & p[0] & cin);

    assign out = p ^ c;

    assign cout = g[3] | (p[3] & g[2]) | (p[3] & p[2] & g[1]) | (p[3] & p[2] & p[1] & g[0]) | (p[3] & p[2] & p[1] & p[0] & cin);
endmodule

module designaha(
    input wire clk,
    input wire rst,
    input wire in,
    output wire out,
    output wire unloading
);
    reg [8:0] ram_in, ram_out;
    wire [8:0] carrylookahead_out;
    reg [2:0] counter;
    reg [1:0] state;
    wire [1:0] next_state;

    localparam LOAD=0, ADD=1, UNLOAD=2, DONE=3; 

    assign out = carrylookahead_out[0];
    assign unloading = (state == UNLOAD);

    always @(*) begin
        case(state)
            LOAD: next_state = counter == 7 ? ADD: LOAD;
            ADD: next_state = UNLOAD;
            UNLOAD: next_state = counter == 7 ? DONE: UNLOAD;
        endcase
    end

    carrylookahead carrylookahead_instance (
        .in1({ram_in[6], ram_in[4], ram_in[2], ram_in[0]}),
        .in2({ram_in[7], ram_in[5], ram_in[3], ram_in[1]}),
        .cin(ram_in[8]),
        .out(carrylookahead_out[7:0]),
        .cout(carrylookahead_out[8])
    );

    always @(posedge clk) begin
        if(rst) begin
            state <= LOAD;
            counter <= 0;
            ram_in <= 0;
            ram_out <= 0;
        end
        else begin
            counter <= counter + 1;
            state <= next_state;

            if(state == LOAD) begin
                ram_in[7:0] <= ram_in >> 1;
                ram_in[8] <= in; 
            end
            else if(state == ADD) begin
                ram_out <= carrylookahead_out;
            end
            else if(state == UNLOAD) begin
                ram_out <= ram_out >> 1;
            end
        end
    end
endmodule

module tb_design;
    reg clk, rst, in;
    wire out, unloading;

    designaha dut_designaha (
        .clk(clk),
        .rst(rst),
        .in(in),
        .out(out),
        .unloading(unloading)
    );

    initial begin
        clk = 0;
        in = 0;
        rst = 1;

        #5 rst = 0;
            in = 1;

        #10 in = 1;
        #10 in = 0;
        #10 in = 1;
        #10 in = 1;
        #10 in = 0;
        #10 in = 1;
        #10 in = 0;
        #10 in = 1;
        
        wait (unloading);

        $monitor("%b", out);
        #1000 $finish;
    end

    always #5 clk = ~clk;
endmodule