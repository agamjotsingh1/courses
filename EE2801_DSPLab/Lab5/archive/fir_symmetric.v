module fir_symmetric #(
    parameter NUM_TAPS = 100,
    parameter INT_NBITS = 2,
    parameter FRAC_NBITS = 14,
    localparam DATA_WIDTH = INT_NBITS + FRAC_NBITS,
    localparam HALF_TAPS = NUM_TAPS / 2
)(
    input wire clk,
    input wire rst,
    input wire en,
    input wire [DATA_WIDTH-1:0] data_in,
    input wire [NUM_TAPS*DATA_WIDTH-1:0] coeff_in,
    output wire [DATA_WIDTH-1:0] data_out,
    output wire data_valid
);

    reg signed [DATA_WIDTH-1:0] x_shift [0:NUM_TAPS-1];
    reg en_shift [0:NUM_TAPS-1];

    reg signed [DATA_WIDTH:0] pre_add [0:HALF_TAPS-1]; 
    reg signed [DATA_WIDTH-1:0] coeff_tap [0:HALF_TAPS-1];
    reg signed [2*DATA_WIDTH:0] mult_full [0:HALF_TAPS-1];
    reg signed [DATA_WIDTH-1:0] mult_trunc [0:HALF_TAPS-1];
    
    reg signed [DATA_WIDTH-1:0] accum_next;
    reg signed [DATA_WIDTH-1:0] data_out_reg;
    reg data_valid_reg;

    integer i;

    assign data_out = data_out_reg;
    assign data_valid = data_valid_reg;

    always @(*) begin
        accum_next = 0;
        for (i = 0; i < HALF_TAPS; i = i + 1) begin
            coeff_tap[i]  = coeff_in[i*DATA_WIDTH +: DATA_WIDTH];
            pre_add[i]    = x_shift[i] + x_shift[NUM_TAPS - 1 - i];
            
            mult_full[i]  = pre_add[i] * coeff_tap[i];
            mult_trunc[i] = mult_full[i] >>> FRAC_NBITS;
            
            accum_next    = accum_next + mult_trunc[i];
        end
    end

    always @(posedge clk or posedge rst) begin
        if (rst) begin
            data_out_reg <= 0;
            data_valid_reg <= 0;
            for (i = 0; i < NUM_TAPS; i = i + 1) begin
                x_shift[i]  <= 0;
                en_shift[i] <= 0;
            end
        end else begin
            data_out_reg <= accum_next;
            data_valid_reg <= en_shift[0]; 
            
            x_shift[0]  <= data_in;
            en_shift[0] <= en;
            for (i = 1; i < NUM_TAPS; i = i + 1) begin
                x_shift[i]  <= x_shift[i-1];
                en_shift[i] <= en_shift[i-1];
            end
        end
    end

endmodule
