`timescale 1ns / 1ps
`include "config.vh"

module tb_divider;
    localparam LUT_SIZE    = 1 << `INDEXING;
    localparam INT_NBITS   = `INT_NBITS;
    localparam FRAC_NBITS  = `FRAC_NBITS;
    localparam NR_ITERS    = `NR_ITERS;
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;

    reg clk;
    reg rst;
    reg [TOTAL_NBITS-1:0] num1;
    reg [TOTAL_NBITS-1:0] num2;
    wire [TOTAL_NBITS-1:0] out;
    wire done;

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    fp_div #(
        .LUT_SIZE(LUT_SIZE),
        .INT_NBITS1(INT_NBITS),
        .FRAC_NBITS1(FRAC_NBITS),
        .INT_NBITS2(INT_NBITS),
        .FRAC_NBITS2(FRAC_NBITS),
        .NR_ITERS(NR_ITERS)
    ) uut (
        .clk(clk),
        .rst(rst),
        .num1(num1),
        .num2(num2),
        .done(done),
        .out(out)
    );

    integer fd_in, fd_out, scan_status;
    reg [8*100:1] header_line;

    initial begin
        rst = 0;
        
        fd_in = $fopen("testing/tests.csv", "r");
        if (fd_in == 0) begin
            $display("ERROR: Could not open testing/tests.csv for reading.");
            $finish;
        end

        fd_out = $fopen("testing/results.csv", "w");
        if (fd_out == 0) begin
            $display("ERROR: Could not open testing/results.csv for writing.");
            $fclose(fd_in);
            $finish;
        end

        scan_status = $fgets(header_line, fd_in);
        $fwrite(fd_out, "num1,num2,div\n");

        // align inputs to the falling edge of the clock for clean setup times
        @(negedge clk); 

        while (!$feof(fd_in)) begin
            scan_status = $fscanf(fd_in, "%h,%h\n", num1, num2);
            if (scan_status == 2) begin
                
                rst = 1;
                @(negedge clk);
                rst = 0;

                wait(done == 1'b1);
                @(negedge clk); 
                
                $fwrite(fd_out, "%0h,%0h,%0h\n", num1, num2, out);
            end
        end

        $fclose(fd_in);
        $fclose(fd_out);
        
        $display("Verilog testbench complete, data written to testing/results.csv.");
        $finish;
    end
endmodule