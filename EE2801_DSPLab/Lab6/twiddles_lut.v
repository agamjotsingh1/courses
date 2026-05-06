//AUTO-GENERATED FILE DO NOT EDIT!
module twiddles_lut #(
    parameter N = 8,
    parameter INT_NBITS = 6,
    parameter FRAC_NBITS = 12
) (
    input wire [1:0] exp,
    output reg [35:0] out
);

    always @(*) begin
        case (exp)
            2'd0: out = 36'h040000000;
            2'd1: out = 36'h02D43F4B0;
            2'd2: out = 36'h00003F000;
            2'd3: out = 36'hFD2C3F4B0;
            default: out = 36'h0;
        endcase
    end

endmodule
