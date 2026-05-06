`timescale 1ns/1ps

module tb_fir_direct;

    parameter NUM_TAPS = 100;
    parameter INT_NBITS = 2;
    parameter FRAC_NBITS = 14;
    localparam DATA_WIDTH = INT_NBITS + FRAC_NBITS;

    reg clk;
    reg rst;
    reg en;
    reg next;
    reg [DATA_WIDTH-1:0] data_in;
    reg [NUM_TAPS*DATA_WIDTH-1:0] coeff_in;

    wire [DATA_WIDTH-1:0] data_out;
    wire data_valid;

    integer file_sig, file_out, status;
    reg [DATA_WIDTH-1:0] temp_coeffs [0:NUM_TAPS-1];
    integer i, flush_count;

    // Instantiating the pipelined FIR module
    fir_direct #(
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

    initial clk = 0;
    always #5 clk = ~clk;

    // Task to process individual signal files
    task process_file;
        input [255:0] in_filename;
        input [255:0] out_filename;
        begin
            $display("Processing file: %0s -> %0s", in_filename, out_filename);
            file_sig = $fopen(in_filename, "r");
            file_out = $fopen(out_filename, "w");

            if (file_sig == 0) begin
                $display("Fatal: Could not open %0s", in_filename);
                $finish;
            end

            rst = 1;
            en = 0;
            next = 0;
            data_in = 0;
            
            #20 rst = 0;

            status = $fscanf(file_sig, "%h", data_in);
            while (status == 1) begin
                en = 1;
                next = 0;
                
                // The TB automatically waits the extra pipeline cycle here
                @(posedge data_valid);
                
                $fdisplay(file_out, "%04h", data_out);
                
                @(negedge clk);
                next = 1;
                @(negedge clk);
                next = 0;
                
                status = $fscanf(file_sig, "%h", data_in);
            end

            // Flush the shift register
            data_in = 0;
            for (flush_count = 0; flush_count < NUM_TAPS - 1; flush_count = flush_count + 1) begin
                en = 1;
                next = 0;
                
                @(posedge data_valid);
                
                $fdisplay(file_out, "%04h", data_out);
                
                @(negedge clk);
                next = 1;
                @(negedge clk);
                next = 0;
            end

            $fclose(file_sig);
            $fclose(file_out);
        end
    endtask

    initial begin
        // Load coefficients
        $readmemh("data/coeffs.hex", temp_coeffs);
        for (i = 0; i < NUM_TAPS; i = i + 1) begin
            coeff_in[i*DATA_WIDTH +: DATA_WIDTH] = temp_coeffs[i];
        end

        // Process test vectors, outputting to new "pipelined" files
        process_file("data/sig1.hex", "data/out_direct_sig1.hex");
        process_file("data/sig2.hex", "data/out_direct_sig2.hex");
        process_file("data/sig3.hex", "data/out_direct_sig3.hex");

        $display("All pipelined simulations complete.");
        $finish;
    end

endmodule