`timescale 1ns/1ps

module tb_fir_symmetric;

    parameter NUM_TAPS = 100;
    parameter INT_NBITS = 2;
    parameter FRAC_NBITS = 14;
    parameter DATA_WIDTH = INT_NBITS + FRAC_NBITS;

    reg clk;
    reg rst;
    reg en;
    reg next;
    reg [DATA_WIDTH-1:0] data_in;
    reg [NUM_TAPS*DATA_WIDTH-1:0] coeff_in;

    wire [DATA_WIDTH-1:0] data_out;
    wire data_valid;

    fir_symmetric #(
        .NUM_TAPS(NUM_TAPS),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) dut (
        .clk(clk),
        .rst(rst),
        .en(en),
        .next(next),
        .data_in(data_in),
        .coeff_in(coeff_in),
        .data_out(data_out),
        .data_valid(data_valid)
    );

    reg [DATA_WIDTH-1:0] coeff_mem [0:NUM_TAPS-1];
    reg [DATA_WIDTH-1:0] temp_data;
    
    integer sig_file;
    integer out_file;
    integer scan_ret;
    integer i;

    initial begin
        clk = 0;
        forever #5 clk = ~clk;
    end

    task process_sample(input [DATA_WIDTH-1:0] sample_in);
        begin
            data_in = sample_in;
            next = 0;
            
            wait (data_valid == 1'b1);
            $fdisplay(out_file, "%04x", data_out);
            
            @(posedge clk);
            next = 1;
            
            wait (data_valid == 1'b0);
            @(posedge clk);
        end
    endtask

    task process_file(input [2047:0] sig_filename, input [2047:0] out_filename);
        begin
            rst = 1;
            en = 0;
            #20;
            rst = 0;
            en = 1;

            sig_file = $fopen(sig_filename, "r");
            if (!sig_file) begin
                $display("Error: Could not open %s", sig_filename);
                $finish;
            end

            out_file = $fopen(out_filename, "w");
            if (!out_file) begin
                $display("Error: Could not open %s", out_filename);
                $finish;
            end

            while (!$feof(sig_file)) begin
                scan_ret = $fscanf(sig_file, "%h\n", temp_data);
                if (scan_ret == 1) begin
                    process_sample(temp_data);
                end
            end

            for (i = 0; i < NUM_TAPS - 1; i = i + 1) begin
                process_sample({DATA_WIDTH{1'b0}});
            end

            $fclose(sig_file);
            $fclose(out_file);
            $display("Simulation complete for %s", sig_filename);
        end
    endtask

    initial begin
        rst = 1;
        en = 0;
        next = 0;
        data_in = 0;
        coeff_in = 0;

        $readmemh("data/coeffs.hex", coeff_mem);
        for (i = 0; i < NUM_TAPS; i = i + 1) begin
            coeff_in[i*DATA_WIDTH +: DATA_WIDTH] = coeff_mem[i];
        end

        process_file("data/sig1.hex", "data/out_symmetric_sig1.hex");
        process_file("data/sig2.hex", "data/out_symmetric_sig2.hex");
        process_file("data/sig3.hex", "data/out_symmetric_sig3.hex");

        $display("All files processed successfully.");
        $finish;
    end

endmodule