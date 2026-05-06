`timescale 1ns / 1ps

module tb_priority_encoder;

    // Inputs
    reg [3:0] in;

    // Outputs
    wire [1:0] out;
    wire valid;

    // Instantiate the Design Under Test (DUT)
    priority_encoder uut (
        .in(in),
        .out(out),
        .valid(valid)
    );

    // VCD generation
    initial begin
        $dumpfile("priority_encoder.vcd");
        $dumpvars(0, tb_priority_encoder);
    end

    // Task to display the output nicely
    task display_outputs;
        begin
            $display("in = %b -> out = %b, valid = %b", in, out, valid);
        end
    endtask

    initial begin
        $display("Starting priority encoder testbench...");
        $monitor("Time %0t: in = %b -> out = %b, valid = %b", $time, in, out, valid);

        // Test all input combinations from 0000 to 1111
        for (integer i = 0; i < 16; i = i + 1) begin
            in = i[3:0];
            #10; // wait 10 time units
        end

        $display("Testbench complete.");
        $finish;
    end

endmodule
