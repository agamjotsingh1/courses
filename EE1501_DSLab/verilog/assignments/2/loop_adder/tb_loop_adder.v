`timescale 1ns/1ns

module tb_loop_adder;
    reg [7:0] a;
    reg [7:0] b;
    reg cin;
    wire [7:0] sum;
    wire cout;

    loop_adder dut(.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    initial begin
        $dumpfile("loop_adder.vcd");
        $dumpvars(0, tb_loop_adder);
        $monitor("input1 = %b, input2 = %b, carry in = %b, sum = %b, carry out = %b", a, b, cin, sum, cout);

        a = 8'd0; b = 8'd0; cin = 1'b0;
        #50 a = 8'd15; b = 8'd15; cin = 1'b0;
        #50 a = 8'd10; b = 8'd5; cin = 1'b1;
        #50 a = 8'd255; b = 8'd1; cin = 1'b0;
        #50 a = 8'd165; b = 8'd90; cin = 1'b0;
        #50;
        /*#50 a = 8'd255; b = 8'd255; cin = 1'b1;
        #50 a = 8'd0; b = 8'd170; cin = 1'b0;
        #50 a = 8'd0; b = 8'd0; cin = 1'b1;
        #50 a = 8'd135; b = 8'd121; cin = 1'b0;
        #50 a = 8'd254; b = 8'd1; cin = 1'b0;

        repeat(5) begin
            a = $random; b = $random; cin = $random % 2; #50;
        end*/

        $finish;
    end
endmodule
