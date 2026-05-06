`timescale 1ns/1ps

module tb_up_counter;

    reg clk;
    reg reset;
    reg enable;
    wire [3:0] count;

    // Instantiate DUT
    up_counter dut (
        .clk(clk),
        .reset(reset),
        .enable(enable),
        .count(count)
    );

    // Clock generator: 10ns period
    always #5 clk = ~clk;

    initial begin
        $dumpfile("up_counter.vcd");
        $dumpvars(0, tb_up_counter);

        // Initialize inputs
        clk = 0;
        reset = 1;
        enable = 0;

        // Apply reset
        #10;
        reset = 0;
        enable = 1;

        // Run counter for a while
        #100;

        // Disable counting
        enable = 0;
        #20;

        // Re-enable counting
        enable = 1;
        #70;

        // Reset during operation
        reset = 1;
        #10;
        reset = 0;

        #40;
        $finish;
    end
endmodule
