module datagen (
    input  wire        clk,
    input  wire        reset,
    input  wire        next_sample_en, // Connected to filter's outputReady
    output wire [15:0] signal_out
);

    // Updated to 14 bits to support 10,000 samples
    reg [13:0] address;

    // Internal address counter hidden from the top level
    always @(posedge clk) begin
        if (reset) begin
            address <= 14'd0;
        end else if (next_sample_en) begin
            // Rollover at 9999 for 10,000 total samples
            if (address == 14'd9999)
                address <= 14'd0;
            else
                address <= address + 14'd1;
        end
    end

    // The ROM IP generated in Quartus
    datagen_rom u0 (
        .address (address),
        .clock   (clk),
        .q       (signal_out)
    );

endmodule