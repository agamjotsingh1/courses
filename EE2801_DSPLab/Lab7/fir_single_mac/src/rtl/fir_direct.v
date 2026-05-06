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
    output wire [DATA_WIDTH-1:0] data_out,
    output reg data_valid
);
    localparam IDLE = 2'b00, DOING = 2'b01, DONE = 2'b10;

    wire [NUM_TAPS*DATA_WIDTH-1:0] coeff_in = {16'h0000,
16'h0001,
16'h0002,
16'h0003,
16'h0004,
16'h0005,
16'h0006,
16'h0008,
16'h000b,
16'h000d,
16'h0010,
16'h0014,
16'h0018,
16'h001d,
16'h0023,
16'h0029,
16'h002f,
16'h0037,
16'h003f,
16'h0048,
16'h0052,
16'h005c,
16'h0067,
16'h0072,
16'h007e,
16'h008b,
16'h0098,
16'h00a5,
16'h00b3,
16'h00c1,
16'h00cf,
16'h00dd,
16'h00eb,
16'h00f9,
16'h0107,
16'h0115,
16'h0122,
16'h012f,
16'h013b,
16'h0147,
16'h0152,
16'h015c,
16'h0165,
16'h016d,
16'h0174,
16'h017a,
16'h017f,
16'h0182,
16'h0185,
16'h0186,
16'h0186,
16'h0185,
16'h0182,
16'h017f,
16'h017a,
16'h0174,
16'h016d,
16'h0165,
16'h015c,
16'h0152,
16'h0147,
16'h013b,
16'h012f,
16'h0122,
16'h0115,
16'h0107,
16'h00f9,
16'h00eb,
16'h00dd,
16'h00cf,
16'h00c1,
16'h00b3,
16'h00a5,
16'h0098,
16'h008b,
16'h007e,
16'h0072,
16'h0067,
16'h005c,
16'h0052,
16'h0048,
16'h003f,
16'h0037,
16'h002f,
16'h0029,
16'h0023,
16'h001d,
16'h0018,
16'h0014,
16'h0010,
16'h000d,
16'h000b,
16'h0008,
16'h0006,
16'h0005,
16'h0004,
16'h0003,
16'h0002,
16'h0001,
16'h0000};

    reg [1:0] state;
    reg [31:0] count;
    reg [DATA_WIDTH-1:0] x [0:NUM_TAPS-1];

    wire [DATA_WIDTH-1:0] prod;
    wire [DATA_WIDTH-1:0] next_accum;

    reg [DATA_WIDTH-1:0] accum;
    assign data_out = accum;

    fp_mul #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) fp_mul_instance (
        .num1(x[count]),
        .num2(coeff_in[count*DATA_WIDTH +: DATA_WIDTH]),
        .out(prod)
    );

    fp_add #(
        .INT_NBITS1(INT_NBITS),
        .FRAC_NBITS1(FRAC_NBITS),
        .INT_NBITS2(INT_NBITS),
        .FRAC_NBITS2(FRAC_NBITS)
    ) fp_add_instance (
        .num1(prod),
        .num2(accum),
        .out(next_accum)
    );

    integer i;

    always @(posedge clk or posedge rst) begin
        if(rst) begin
            state <= IDLE;
            count <= 0;
            accum <= 0;
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
                    accum <= 0;
                    data_valid <= 1'b0;
                end
                DOING: begin
                    count <= count + 1;
                    accum <= next_accum;
                    if(count == NUM_TAPS - 1) begin
                        state <= IDLE;
                        data_valid <= 1'b1;
                    end
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
