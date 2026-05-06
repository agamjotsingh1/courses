module reorder_buf #(
    parameter N = 8,
    parameter INT_NBITS = 3,
    parameter FRAC_NBITS = 5
) (
    input wire clk,
    input wire rst,
    input wire en,
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] in,
    output reg [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out,
    output reg out_valid
);
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;
    localparam WORD_WIDTH  = 2 * TOTAL_NBITS;
    localparam ADDR_WIDTH  = $clog2(N);

    // pingpong memory -> 2 banks of size N
    reg [WORD_WIDTH-1:0] ram [0 : 2*N - 1];

    reg [ADDR_WIDTH-1:0] count;

    reg bank_sel;
    reg first_frame_done;

    wire [ADDR_WIDTH-1:0] read_addr_rev;
    wire [ADDR_WIDTH:0]   write_addr;
    wire [ADDR_WIDTH:0]   read_addr;

    genvar i;
    generate
        for (i = 0; i < ADDR_WIDTH; i = i + 1) begin : bit_rev
            assign read_addr_rev[ADDR_WIDTH - 1 - i] = count[i];
        end
    endgenerate

    assign write_addr = {bank_sel, count};
    assign read_addr  = {~bank_sel, read_addr_rev};

    always @(posedge clk) begin
        if (rst) begin
            count <= 0;
            bank_sel <= 1'b0;
            first_frame_done <= 1'b0;
            out_valid <= 1'b0;
            out <= 0;
        end else if (en) begin
            ram[write_addr] <= in;

            out <= ram[read_addr];
            out_valid <= first_frame_done;

            if (count == N - 1) begin
                count <= 0;
                bank_sel <= ~bank_sel;
                first_frame_done <= 1'b1;
            end else begin
                count <= count + 1;
            end
        end
    end

endmodule