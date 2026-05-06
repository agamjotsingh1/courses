`timescale 1ns / 1ps

module tb_guess;

    // Parameters for Q(16, 16)
    localparam LUT_SIZE    = 64;
    localparam INT_NBITS   = 16;
    localparam FRAC_NBITS  = 16;
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;

    // UUT Signals
    reg  [TOTAL_NBITS-1:0] denom;
    wire [TOTAL_NBITS-1:0] out;

    // Variable to hold the real-format representation
    real denom_real;

    // Instantiate the Unit Under Test (UUT)
    guess #(
        .LUT_SIZE(LUT_SIZE),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) uut (
        .denom(denom),
        .out(out)
    );

    // Helper task to apply values, wait, and print
    task apply_test;
        input [TOTAL_NBITS-1:0] test_val;
        begin
            denom = test_val;
            #5; // Wait for combinational logic to evaluate
            
            // Convert unsigned Q16.16 fixed-point to real
            // 2^16 = 65536.0
            denom_real = denom / 65536.0;
            
            // Print denom in real (%f) and guess in integer (%0d)
            $display("denom = %8.4f | guess = %0d", denom_real, out);
        end
    endtask

    initial begin
        $display("Starting Q(16,16) Guess Module Simulation...");
        $display("---------------------------------------------------");
        
        // Test 1: 1.0 (1 << 16 = 32'h0001_0000)
        apply_test(32'h0001_0000);
        
        // Test 2: 2.5 (2.5 * 65536 = 32'h0002_8000)
        apply_test(32'h0002_8000);
        
        // Test 3: 0.25 (0.25 * 65536 = 32'h0000_4000)
        apply_test(32'h0000_4000);
        
        // Test 4: 10.125 (10.125 * 65536 = 32'h000A_2000)
        apply_test(32'h000A_2000);
        
        // Test 5: A small fractional value like 0.03125
        apply_test(32'h0000_0800);

        apply_test(32'h001D_0000);
        
        $display("---------------------------------------------------");
        $finish;
    end

endmodule
