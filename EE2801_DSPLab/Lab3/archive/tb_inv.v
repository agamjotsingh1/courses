`timescale 1ns / 1ps
`include "config.vh"

module tb_inv;
    localparam LUT_SIZE    = 1 << `INDEXING; 
    localparam INT_NBITS   = `INT_NBITS;
    localparam FRAC_NBITS  = `FRAC_NBITS;
    localparam NR_ITERS    = `NR_ITERS;
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;

    reg  [TOTAL_NBITS-1:0] denom;
    wire [TOTAL_NBITS-1:0] out;

    real denom_real;
    real out_real;

    // Instantiate the Unit Under Test (UUT)
    fp_inv #(
        .LUT_SIZE(LUT_SIZE),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS),
        .NR_ITERS(NR_ITERS)
    ) uut (
        .denom(denom),
        .out(out)
    );

    // Helper task to apply values, wait, and print
    task apply_test;
        input [TOTAL_NBITS-1:0] test_val;
        begin
            denom = test_val;
            #10; // Wait for combinational logic to evaluate
            
            // Convert unsigned Q16.16 fixed-point to real (2^16 = 65536.0)
            denom_real = denom / 65536.0;
            out_real   = out / 65536.0;
            
            // Print denom (real), out (int), and out (real) to verify the math
            $display("denom = %8.4f | out (int) = %10d | out (real) = %8.4f", 
                     denom_real, out, out_real);
        end
    endtask

    initial begin
        $display("Starting fp_divide (Newton-Raphson) Simulation...");
        $display("------------------------------------------------------------------");
        
        // Test 1: 1.0 -> Expected output: 1.0 (32'h0001_0000)
        apply_test(32'h0001_0000);
        
        // Test 2: 2.0 -> Expected output: 0.5 (32'h0000_8000)
        apply_test(32'h0002_0000);
        
        // Test 3: 4.0 -> Expected output: 0.25 (32'h0000_4000)
        apply_test(32'h0004_0000);
        
        // Test 4: 10.0 -> Expected output: 0.1 (32'h0000_1999 approx)
        apply_test(32'h000A_0000);

        // Test 5: 0.5 -> Expected output: 2.0 (32'h0002_0000)
        apply_test(32'h0000_8000);

        // Test 6: 3.125 -> Expected output: 0.32 (32'h0000_51EB approx)
        apply_test(32'h0003_2000);

        apply_test(32'h001D_0000);
        apply_test(32'h0000_0100);
        
        $display("------------------------------------------------------------------");
        $finish;
    end

endmodule