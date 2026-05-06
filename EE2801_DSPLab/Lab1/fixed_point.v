module fixed_point #(
    parameter INT_NBITS  = 2,
    parameter FRAC_NBITS = 14
)(
    input wire [63:0] float,
    output wire [INT_NBITS-1:0] int_bits,
    output wire [FRAC_NBITS-1:0] frac_bits
);
    localparam EXP_BIAS = 1023;
    localparam EXP_NBITS = 11;
    localparam MANT_NBITS = 52;
    localparam SIGNIF_NBITS = MANT_NBITS + 1;

    // INT_NBITS - (2) is added to make the decimal point in the right place
    // why 2? because in the floating point representation it is 1.<mantissa>
    // and we need another buffer bit which we will use to manage sign and take
    // two's complement later
    localparam SHIFT_CONST = EXP_BIAS + (INT_NBITS - 2);

    localparam TOTAL_NBITS = INT_NBITS + FRAC_NBITS;
    localparam REDUCED_NBITS = TOTAL_NBITS - 1;

    wire sign = float[63];
    wire [EXP_NBITS-1:0] exponent = float[62:52];
    wire [MANT_NBITS-1:0] mantissa = float[51:0];

    // for denormal numbers, significand = 0.<mantissa>
    // normally, significand = 1.<mantissa>
    wire [SIGNIF_NBITS-1:0] significand = {(exponent != 0), mantissa};

    reg [TOTAL_NBITS-1:0] fixed_point_repr;
    reg [(2*(REDUCED_NBITS) - 1):0] shifted_fixed_point_repr;
    reg [(2*(TOTAL_NBITS) - 1):0] unsigned_fixed_point_repr;
    reg [(2*(REDUCED_NBITS) - 1):0] extended_fixed_point_repr;
    reg rounding_compensation;

    always @(*) begin
        extended_fixed_point_repr = 0;

        // extended repr = {<fixed point repr>, <extra bits that may flow>}
        // truncate/extract twice as many bits in the fixed point case
        // reason: after shifting other bits will flow into the upper half (fixed point repr)
        if(2*REDUCED_NBITS > SIGNIF_NBITS) begin
            extended_fixed_point_repr[(2*(REDUCED_NBITS) - 1) -: SIGNIF_NBITS] = significand[SIGNIF_NBITS-1:0];
        end
        else begin
            extended_fixed_point_repr[(2*(REDUCED_NBITS) - 1):0] = significand[(SIGNIF_NBITS - 1) -: 2*(REDUCED_NBITS)];
        end

        // avoid numbers which are too big for the fixed point representation to handle
        // just take the maximum possible if out of range
        if(exponent < (INT_NBITS - 1) + EXP_BIAS) begin
            // shift the extended fixed point representation
            // by enough to make it so that the top bits of shifted_fixed_point_repr
            // are one less than INT_NBITS (to handle sign later) are the integer bits
            // and lower FRAC_NBITS are the fraction bits
            shifted_fixed_point_repr = (exponent >= SHIFT_CONST) ? 
                extended_fixed_point_repr << (exponent - SHIFT_CONST):
                (
                    // fixing denormal numbers
                    exponent == 0 ? 
                    extended_fixed_point_repr >> (SHIFT_CONST - 1):
                    extended_fixed_point_repr >> (SHIFT_CONST - exponent)
                );

            // without this, it would basically be a floor and SQNR from python won't match approximately
            rounding_compensation = shifted_fixed_point_repr[REDUCED_NBITS - 1];

            // first bit zero to later manage sign
            unsigned_fixed_point_repr = {1'b0, shifted_fixed_point_repr[(2*(REDUCED_NBITS) - 1) -: REDUCED_NBITS]
                                        + rounding_compensation};

            // take twos complement if number is negative
            fixed_point_repr = sign ? ((~unsigned_fixed_point_repr + 1)): unsigned_fixed_point_repr;
        end
        else begin
            // clip to the max/min value depending on sign
            fixed_point_repr = sign ? {1'b1, {(TOTAL_NBITS - 1){1'b0}}}: {1'b0, {(TOTAL_NBITS - 1){1'b1}}};
        end
    end

    assign int_bits = fixed_point_repr[(TOTAL_NBITS-1) -: INT_NBITS];
    assign frac_bits = fixed_point_repr[0 +: FRAC_NBITS];
endmodule