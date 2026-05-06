module fp_inv #(
    parameter LUT_SIZE,
    parameter INT_NBITS,
    parameter FRAC_NBITS,
    parameter NR_ITERS
) (
    input wire clk,
    input wire rst,
    input wire [(INT_NBITS + FRAC_NBITS - 1):0] denom,

    output wire done,
    output wire [(INT_NBITS + FRAC_NBITS - 1):0] out
);
    reg [(INT_NBITS + FRAC_NBITS - 1):0] x;
    wire [(INT_NBITS + FRAC_NBITS - 1):0] x_guess, x_nr;

    localparam COUNT_NBITS = 64;

    reg [COUNT_NBITS-1:0] count;

    always @(posedge clk) begin
        if(rst) begin
            x <= x_guess;
            count <= 1'b0;
        end
        else if(done == 0) begin
            x <= x_nr;
            count <= count + 1;
        end
    end

    assign done = (count == NR_ITERS);

    guess #(
        .LUT_SIZE(LUT_SIZE),
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) guess_instance (
        .denom(denom),
        .out(x_guess)
    );

    newton_raphson #(
        .INT_NBITS(INT_NBITS),
        .FRAC_NBITS(FRAC_NBITS)
    ) newton_raphson_iter (
        .current(x),
        .denom(denom),
        .out(x_nr)
    );
    
    assign out = x;
endmodule