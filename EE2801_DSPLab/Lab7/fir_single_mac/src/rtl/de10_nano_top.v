module de10_nano_top (
    input wire FPGA_CLK1_50,
    input wire [1:0] KEY
);

    wire clk = FPGA_CLK1_50;
    wire reset = ~KEY[0]; 
    
    (* keep *) wire [15:0] test_signal;
    (* keep *) wire [15:0] filtered_signal;
    (* keep *) wire        sample_sync;

    // Instantiate the hidden data generator
    datagen u_source (
        .clk            (clk),
        .reset          (reset),
        .next_sample_en (sample_sync), // Feed back the sync pulse
        .signal_out     (test_signal)
    );

    // Instantiate the FIR Filter
    fir_symmetric_pipelined #(
        .INT_NBITS(2),
        .FRAC_NBITS(14),
        .NUM_TAPS(100)
    ) u_fir (
        .clk        (clk),
        .rst        (reset),
        .en         (1'b1),
        .next       (sample_sync),
        .data_in    (test_signal),
        .data_out   (filtered_signal),
        .data_valid (sample_sync) // Sync pulse triggers next sample
    );

endmodule