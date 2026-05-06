`timescale 1ns / 1ps

module tb_fft;
    localparam N = 8;
    localparam NUM_FRAMES = 5;
    localparam INT_NBITS = 6;
    localparam FRAC_NBITS = 12;
    localparam TOTAL_NBITS = 2 * (INT_NBITS + FRAC_NBITS);

    reg clk;
    reg rst;
    reg en;
    reg [TOTAL_NBITS-1:0] in;
    wire [TOTAL_NBITS-1:0] out;
    wire out_valid;

    reg [TOTAL_NBITS-1:0] in_mem [0:(NUM_FRAMES * N) - 1];
    integer fd_out [0:NUM_FRAMES-1];
    
    integer i;
    integer out_count;
    integer file_idx;

    fft #(
        .N(N),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) dut (
        .clk(clk),
        .rst(rst),
        .en(en),
        .in(in),
        .out(out),
        .out_valid(out_valid)
    );

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        $readmemh("sig1.hex", in_mem, 0, 7);
        $readmemh("sig2.hex", in_mem, 8, 15);
        $readmemh("sig3.hex", in_mem, 16, 23);
        $readmemh("sig4.hex", in_mem, 24, 31);
        $readmemh("sig5.hex", in_mem, 32, 39);

        fd_out[0] = $fopen("out_sig1.hex", "w");
        fd_out[1] = $fopen("out_sig2.hex", "w");
        fd_out[2] = $fopen("out_sig3.hex", "w");
        fd_out[3] = $fopen("out_sig4.hex", "w");
        fd_out[4] = $fopen("out_sig5.hex", "w");

        rst = 1;
        en = 0;
        in = 0;
        out_count = 0;
        file_idx = 0;

        @(posedge clk);
        @(posedge clk);
        rst <= 0;
        en <= 1;

        // Feed data continuously to fully utilize the pipeline
        for (i = 0; i < (NUM_FRAMES * N); i = i + 1) begin
            in <= in_mem[i];
            @(posedge clk);
        end
        
        in <= 0;
    end

    always @(negedge clk) begin
        if (!rst && out_valid) begin
            $fdisplay(fd_out[file_idx], "%04x", out);
            out_count = out_count + 1;
            
            // Switch to the next file when a frame completes
            if (out_count == N) begin
                out_count = 0;
                $fclose(fd_out[file_idx]);
                file_idx = file_idx + 1;
                
                if (file_idx == NUM_FRAMES) begin
                    $finish;
                end
            end
        end
    end

endmodule