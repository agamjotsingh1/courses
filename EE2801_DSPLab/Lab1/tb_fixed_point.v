`timescale 1ns/1ps
`define PI 3.141592653589793

module tb_fixed_point;
    // x(t) = 2sin(2*pi*f*t)
    real f    = 1e3;
    real f_s  = 48e3; // sampling frequency
    real duration = 1;
    integer NSAMPLES = duration * f_s;

    // IEEE double representation
    reg [63:0] x_bits;

    reg [1:0] int_q2_14;
    reg [13:0] frac_q2_14;

    reg [3:0] int_q4_12;
    reg [11:0] frac_q4_12;

    reg [7:0] int_q8_4;
    reg [3:0] frac_q8_4;

    fixed_point #(.INT_NBITS(2), .FRAC_NBITS(14)) dut_q2_14 (
        .float(x_bits),
        .int_bits(int_q2_14),
        .frac_bits(frac_q2_14)
    );

    fixed_point #(.INT_NBITS(4), .FRAC_NBITS(12)) dut_q4_12 (
        .float(x_bits),
        .int_bits(int_q4_12),
        .frac_bits(frac_q4_12)
    );

    fixed_point #(.INT_NBITS(8), .FRAC_NBITS(4)) dut_q8_4 (
        .float(x_bits),
        .int_bits(int_q8_4),
        .frac_bits(frac_q8_4)
    );

    integer f_q2_14, f_q4_12, f_q8_4; // file handles

    real    t;
    real    x_real;

    function real fixed_to_float;
        input integer int_part;
        input integer frac_part;
        input integer frac_bits;
    begin
        fixed_to_float = int_part + (frac_part / (1.0 * (1 << frac_bits)));
    end
    endfunction

    real q2_14, q4_12, q8_4;
    integer n;

    initial begin
        // writing in csv format
        f_q2_14 = $fopen("data/q2_14.csv", "w");
        f_q4_12 = $fopen("data/q4_12.csv", "w");
        f_q8_4 = $fopen("data/q8_4.csv", "w");

        $fwrite(f_q2_14, "time,original,quantized,error\n");
        $fwrite(f_q4_12, "time,original,quantized,error\n");
        $fwrite(f_q8_4, "time,original,quantized,error\n");

        for (n = 0; n < NSAMPLES; n = n + 1) begin
            t = n * (1.0/f_s);
            x_real = 2 * $sin(2.0 * `PI * f * t);
            x_bits = $realtobits(x_real);

            #1;

            q2_14 = fixed_to_float(
                    $signed(int_q2_14),
                    frac_q2_14,
                    14
                );

            q4_12 = fixed_to_float(
                    $signed(int_q4_12),
                    frac_q4_12,
                    12
                );

            q8_4 = fixed_to_float(
                    $signed(int_q8_4),
                    frac_q8_4,
                    4
                );

            $fwrite(f_q2_14, "%.10f,%.10f,%.10f,%.10f\n",
                    t, x_real, q2_14, (x_real - q2_14));

            $fwrite(f_q4_12, "%.10f,%.10f,%.10f,%.10f\n",
                    t, x_real, q4_12, (x_real - q4_12));

            $fwrite(f_q8_4, "%.10f,%.10f,%.10f,%.10f\n",
                    t, x_real, q8_4, (x_real - q8_4));
        end

        $fclose(f_q2_14);
        $fclose(f_q4_12);
        $fclose(f_q8_4);

        $display("Simulation complete. CSV files generated.");
        $finish;
    end

endmodule
