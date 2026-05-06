`timescale 1ns / 1ps

module tb_fixed_point;
    parameter INT_W1  = 2;
    parameter FRAC_W1 = 14; 
    
    parameter INT_W2  = 4;
    parameter FRAC_W2 = 12;

    parameter ADD_TOTAL_W = ((INT_W1 > INT_W2 ? INT_W1 : INT_W2) + (FRAC_W1 > FRAC_W2 ? FRAC_W1 : FRAC_W2));
    parameter MUL_TOTAL_W = (INT_W1 + INT_W2) + (FRAC_W1 + FRAC_W2);

    integer fd1, fd2, fd_out;
    integer code1, code2;
    reg[1023:0] line1, line2;
    real    t1, orig1, q1, err1; 
    real    t2, orig2, q2, err2; 

    reg [63:0] float_bits_1, float_bits_2;
    wire [INT_W1-1:0] int_part_1; wire [FRAC_W1-1:0] frac_part_1;
    wire [INT_W2-1:0] int_part_2; wire [FRAC_W2-1:0] frac_part_2;

    wire [INT_W1 + FRAC_W1 - 1 : 0] num1_packed = {int_part_1, frac_part_1};
    wire [INT_W2 + FRAC_W2 - 1 : 0] num2_packed = {int_part_2, frac_part_2};

    wire [ADD_TOTAL_W - 1 : 0] sum_out, sub_out;
    wire [MUL_TOTAL_W - 1 : 0] mul_out;
    real real_num1, real_num2, real_sum, real_sub, real_mul;

    fixed_point #(.INT_NBITS(INT_W1), .FRAC_NBITS(FRAC_W1)) conv1 (.float(float_bits_1), .int_bits(int_part_1), .frac_bits(frac_part_1));
    fixed_point #(.INT_NBITS(INT_W2), .FRAC_NBITS(FRAC_W2)) conv2 (.float(float_bits_2), .int_bits(int_part_2), .frac_bits(frac_part_2));

    fixed_point_add #(.INT_NBITS1(INT_W1), .FRAC_NBITS1(FRAC_W1), .INT_NBITS2(INT_W2), .FRAC_NBITS2(FRAC_W2)) 
        adder_inst (.num1(num1_packed), .num2(num2_packed), .out(sum_out));

    fixed_point_sub #(.INT_NBITS1(INT_W1), .FRAC_NBITS1(FRAC_W1), .INT_NBITS2(INT_W2), .FRAC_NBITS2(FRAC_W2)) 
        sub_inst (.num1(num1_packed), .num2(num2_packed), .out(sub_out));

    fixed_point_mul #(.INT_NBITS1(INT_W1), .FRAC_NBITS1(FRAC_W1), .INT_NBITS2(INT_W2), .FRAC_NBITS2(FRAC_W2)) 
        mul_inst (.num1(num1_packed), .num2(num2_packed), .out(mul_out));

    initial begin
        fd1    = $fopen("../Lab1/data/q2_14.csv", "r");
        fd2    = $fopen("../Lab1/data/q4_12.csv", "r");
        fd_out = $fopen("./data/result.csv", "w");

        if (fd1 == 0 || fd2 == 0 || fd_out == 0) begin
            $display("Error: Could not open files.");
            $finish;
        end

        // Write Header to result.csv
        $fdisplay(fd_out, "time,original,q2_14,q4_12,add,sub,mul");

        // Skip input headers
        void'($fgets(line1, fd1));
        void'($fgets(line2, fd2));

        while (!$feof(fd1) && !$feof(fd2)) begin
            code1 = $fgets(line1, fd1);
            code2 = $fgets(line2, fd2);

            if (code1 > 0 && code2 > 0) begin
                $sscanf(line1, "%f,%f,%f,%f", t1, orig1, q1, err1);
                $sscanf(line2, "%f,%f,%f,%f", t2, orig2, q2, err2);

                float_bits_1 = $realtobits(orig1);
                float_bits_2 = $realtobits(orig2);

                #1; // Allow combinational logic to propagate

                real_num1 = $itor($signed(num1_packed)) / (1 << FRAC_W1);
                real_num2 = $itor($signed(num2_packed)) / (1 << FRAC_W2);
                real_sum  = $itor($signed(sum_out)) / (1 << (FRAC_W1 > FRAC_W2 ? FRAC_W1 : FRAC_W2));
                real_sub  = $itor($signed(sub_out)) / (1 << (FRAC_W1 > FRAC_W2 ? FRAC_W1 : FRAC_W2));
                real_mul  = $itor($signed(mul_out)) / (1 << (FRAC_W1 + FRAC_W2));

                $fdisplay(fd_out, "%f,%f,%f,%f,%f,%f,%f", 
                          t1, orig1, real_num1, real_num2, real_sum, real_sub, real_mul);
            end
        end

        $fclose(fd1);
        $fclose(fd2);
        $fclose(fd_out);
        $display("Simulation complete. Data written.");
        $finish;
    end
endmodule