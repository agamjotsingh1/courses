module fir_direct #(
    parameter NUM_TAPS = 100,
    parameter INT_NBITS = 2,
    parameter FRAC_NBITS = 14,
    parameter DATA_WIDTH = INT_NBITS + FRAC_NBITS
)(
    input wire clk,
    input wire rst,
    input wire en,
    input wire next,
    input wire [DATA_WIDTH-1:0] data_in,
    input wire [NUM_TAPS*DATA_WIDTH-1:0] coeff_in,
    output wire [DATA_WIDTH-1:0] data_out,
    output reg data_valid
);
    localparam IDLE = 2'b00, DOING = 2'b01, DONE = 2'b10;

    reg [1:0] state;
    reg [31:0] count;
    reg [31:0] read_addr; 
    reg [DATA_WIDTH-1:0] x [0:NUM_TAPS-1];

    wire [DATA_WIDTH-1:0] prod_wire;
    reg  [DATA_WIDTH-1:0] prod_reg;
    wire [DATA_WIDTH-1:0] next_accum;

    reg [DATA_WIDTH-1:0] accum;
    assign data_out = accum;

    fp_mul #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) fp_mul_instance (
        .num1(x[read_addr]),
        .num2(coeff_in[read_addr*DATA_WIDTH +: DATA_WIDTH]),
        .out(prod_wire)
    );

    fp_add #(
        .INT_NBITS1(INT_NBITS),
        .FRAC_NBITS1(FRAC_NBITS),
        .INT_NBITS2(INT_NBITS),
        .FRAC_NBITS2(FRAC_NBITS)
    ) fp_add_instance (
        .num1(prod_reg),
        .num2(accum),
        .out(next_accum)
    );

    integer i;

    always @(posedge clk or posedge rst) begin
        if(rst) begin
            state <= IDLE;
            count <= 0;
            read_addr <= 0;
            accum <= 0;
            prod_reg <= 0;
            data_valid <= 0;
            for (i=0; i<NUM_TAPS; i=i+1) x[i] <= 0;
        end
        else if(en) begin
            case(state)
                IDLE: begin
                    for (i=0; i<NUM_TAPS-1; i=i+1) x[i+1] <= x[i];
                    x[0] <= data_in;
                    state <= DOING;
                    count <= 0;
                    read_addr <= 0;
                    accum <= 0;
                    prod_reg <= 0;
                end
                DOING: begin
                    count <= count + 1;
                    
                    if (read_addr < NUM_TAPS - 1)
                        read_addr <= read_addr + 1;

                    prod_reg <= prod_wire;
                    accum <= next_accum;
                    
                    if(count == NUM_TAPS) state <= DONE; 
                end
                DONE: begin
                    if(next == 1'b0) begin
                        state <= DONE;
                        data_valid <= 1'b1;
                    end
                    else begin
                        state <=  IDLE;
                        data_valid <= 1'b0;
                    end
                end
            endcase
        end
    end
endmodule
