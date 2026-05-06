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
    wire out_valid;

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
        .out(out),
        .out_valid(out_valid)
    );

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    initial begin
        for (i = 0; i < MEM_DEPTH; i = i + 1) begin
            in_mem[i] = 0;
        end
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
        if (!rst && out_valid) begin
            $fdisplay(fd_out, "%04x", out);
            out_count = out_count + 1;
            
            if (out_count == N) begin
                $fclose(fd_out);
                $finish;
            end
        end
    end

endmodule