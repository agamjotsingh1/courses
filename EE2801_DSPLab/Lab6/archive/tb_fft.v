`timescale 1ns / 1ps

module tb_fft;
    localparam N = 8;
    localparam INT_NBITS = 3;
    localparam FRAC_NBITS = 5;
    localparam TOTAL_NBITS = 2 * (INT_NBITS + FRAC_NBITS);
    localparam MEM_DEPTH = 256; 

    reg clk;
    reg rst;
    reg en;
    reg [TOTAL_NBITS-1:0] in;
    wire [TOTAL_NBITS-1:0] out;

    reg [TOTAL_NBITS-1:0] in_mem [0:MEM_DEPTH-1];
    integer fd_out;
    integer i;
    integer out_count;

    fft #(
        .N(N),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) dut (
        .clk(clk),
        .rst(rst),
        .en(en),
        .in(in),
        .out(out)
    );

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        $readmemh("sig.hex", in_mem);
        
        fd_out = $fopen("output_sig.hex", "w");
        if (!fd_out) begin
            $display("Error opening output_sig.hex");
            $finish;
        end

        rst = 1;
        en = 0;
        in = 0;
        out_count = 0;

        @(posedge clk);
        @(posedge clk);
        rst <= 0;
        en <= 1;

        for (i = 0; i < MEM_DEPTH; i = i + 1) begin
            if (in_mem[i] === {TOTAL_NBITS{1'bx}}) begin
                in <= {TOTAL_NBITS{1'b0}};
            end else begin
                in <= in_mem[i];
            end
            @(posedge clk);
        end
    end

    always @(negedge clk) begin
        if (!rst && en) begin
            if (out_count >= (N - 1)) begin
                $fdisplay(fd_out, "%04x", out);
                
                // Stop after capturing exactly N samples
                if (out_count == (2 * N - 2)) begin
                    $fclose(fd_out);
                    $finish;
                end
            end
            out_count = out_count + 1;
        end
    end

endmodule