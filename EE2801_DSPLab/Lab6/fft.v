module fft #(
    parameter N = 8,
    parameter INT_NBITS = 3,
    parameter FRAC_NBITS = 5
) (
    input wire clk,
    input wire rst,
    input wire en,
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] in,
    output wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out,
    output wire out_valid
);
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;
    localparam STAGES = $clog2(N);

    wire [2*TOTAL_NBITS - 1 : 0] stage_data [0 : STAGES];
    reg [($clog2(N)-1) : 0] count;

    assign stage_data[STAGES] = in;

    genvar i;
    generate
        for (i = STAGES - 1; i >= 0; i = i - 1) begin : fft_stages
            decimator #(
                .N(N),
                .L(i), 
                .INT_NBITS(INT_NBITS),
                .FRAC_NBITS(FRAC_NBITS)
            ) u_decimator (
                .clk(clk),
                .en(en),
                .rst(rst),
                .in(stage_data[i+1]),
                .count(count),
                .out(stage_data[i])
            );
        end
    endgenerate

    always @(posedge clk) begin
        if(rst) begin
            count <= 0;
        end
        else if(en) begin
            count <= count + 1;
        end
    end

    reg [N-2:0] valid_shift;
    always @(posedge clk) begin
        if (rst) valid_shift <= 0;
        else valid_shift <= {valid_shift[N-3:0], en};
    end

    wire stage0_valid = valid_shift[N-2];


    reorder_buf #(
        .N(N),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) u_reorder_buf (
        .clk(clk),
        .rst(rst),
        .en(stage0_valid),
        .in(stage_data[0]),
        .out(out),
        .out_valid(out_valid)
    );
endmodule