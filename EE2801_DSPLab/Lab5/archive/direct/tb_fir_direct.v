`timescale 1ns / 1ps

module tb_fir_direct;

    localparam NUM_TAPS   = 100;
    localparam INT_NBITS  = 2;
    localparam FRAC_NBITS = 14;
    localparam DATA_WIDTH = INT_NBITS + FRAC_NBITS;

    reg clk;
    reg rst;
    reg en;
    reg  [DATA_WIDTH-1:0] data_in;
    reg  [NUM_TAPS*DATA_WIDTH-1:0] coeff_in;

    wire [DATA_WIDTH-1:0] data_out;
    wire data_valid;

    fir_direct #(
        .NUM_TAPS(NUM_TAPS),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) dut (
        .clk(clk),
        .rst(rst),
        .en(en),
        .data_in(data_in),
        .coeff_in(coeff_in),
        .data_out(data_out),
        .data_valid(data_valid)
    );

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    reg [DATA_WIDTH-1:0] coeff_mem [0:NUM_TAPS-1];
    integer fd_in, fd_out, status, i, sig_idx;
    reg [255:0] in_file;
    reg [255:0] out_file;

    initial begin
        $timeformat(-9, 2, " ns", 10);
        $readmemh("data/coeffs.hex", coeff_mem);
        coeff_in = 0;
        for (i = 0; i < NUM_TAPS; i = i + 1) begin
            coeff_in[i*DATA_WIDTH +: DATA_WIDTH] = coeff_mem[i];
        end

        for (sig_idx = 1; sig_idx <= 3; sig_idx = sig_idx + 1) begin
            rst = 1;
            en = 0;
            data_in = 0;
            
            repeat(5) @(posedge clk);
            rst = 0;
            
            $sformat(in_file, "data/sig%0d.hex", sig_idx);
            $sformat(out_file, "data/out_direct_sig%0d.hex", sig_idx);

            fd_in = $fopen(in_file, "r");
            if (fd_in == 0) begin
                $display("Error: Could not open %s", in_file);
                $finish;
            end

            fd_out = $fopen(out_file, "w");
            if (fd_out == 0) begin
                $display("Error: Could not open %s", out_file);
                $finish;
            end

            @(negedge clk);
            en = 1;
            
            status = $fscanf(fd_in, "%h", data_in);
            while (status == 1) begin
                @(negedge clk);
                status = $fscanf(fd_in, "%h", data_in);
            end

            data_in = 0;
            repeat (NUM_TAPS) @(negedge clk);

            en = 0;
            repeat (NUM_TAPS - 1) @(negedge clk);

            $fclose(fd_in);
            $fclose(fd_out);
        end
        
        $display("Simulation finished at %0t", $time);
        $finish;
    end

    always @(posedge clk) begin
        if (!rst && data_valid) begin
            $fdisplay(fd_out, "%04x", data_out);
        end
    end

endmodule