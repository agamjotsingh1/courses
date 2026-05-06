module decimator #(
    parameter N,
    parameter L,
    parameter INT_NBITS,
    parameter FRAC_NBITS
) (
    input wire clk,
    input wire rst,
    input wire en,
    input wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] in,
    input wire [($clog2(N)-1) : 0] count,
    output wire [2*(INT_NBITS + FRAC_NBITS) - 1 : 0] out
);
    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;
    localparam USR_LEN = 2**L;

    wire [2*TOTAL_NBITS - 1 : 0] A, B, A_add_B, A_sub_B;
    wire ctrl = count[L];

    reg [2*TOTAL_NBITS - 1: 0] usr [0:(USR_LEN-1)];

    integer i;
    always @(posedge clk) begin
        if(rst) begin
            for(i = 0; i < USR_LEN; i = i + 1) begin
                usr[i] <= 0;
            end
        end
        else if(en) begin
            usr[0] <= ctrl ? A_sub_B: in;
            for(i = 1; i < USR_LEN; i = i + 1) begin
                usr[i] <= usr[i - 1];
            end
        end
    end

    butterfly #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) u_butterfly (
        .a(usr[USR_LEN - 1]),
        .b(in),
        .out_add(A_add_B),
        .out_sub(A_sub_B)
    );

    wire [$clog2(N/2) - 1 : 0] twiddle_exp;

    generate
        if (L == 0) begin : gen_twiddle
            assign twiddle_exp = 0;
        end else begin : gen_twiddle
            assign twiddle_exp = ctrl ? 0 : (count[L - 1 : 0] << ($clog2(N/2) - L));
        end
    endgenerate

    rotate #(
        .N(N),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) u_rotate (
        .in(ctrl ? A_add_B: usr[USR_LEN - 1]),
        .twiddle_exp(twiddle_exp),
        .out(out)
    );

endmodule