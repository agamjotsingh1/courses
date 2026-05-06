`timescale 1ns/1ns

module tb_ripple_adder_nand;
    reg [3:0] a;
    reg [3:0] b;
    reg cin;
    wire [3:0] sum;
    wire cout;

    ripple_adder_nand dut(.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    initial begin
        $dumpfile("ripple_adder_nand.vcd");
        $dumpvars(0, tb_ripple_adder_nand);
        //$monitor("\na = %b, b = %b, cin = %b\nsum = %b, cout = %b", a, b, cin, sum, cout);

        a = 4'b0000; b = 4'b0000; cin = 1'b0;
        #50 a = 4'b1111; b = 4'b0000; cin = 1'b1;
        #50 a = 4'b1010; b = 4'b0101; cin = 1'b1;
        #50 a = 4'b1111; b = 4'b0001; cin = 1'b0;
        #50 a = 4'b1000; b = 4'b0001; cin = 1'b0;
        #50;
        /*
        #50 a = 4'b1111; b = 4'b1111; cin = 1'b0;
        #50 a = 4'b1010; b = 4'b0101; cin = 1'b0;
        #50 a = 4'b0001; b = 4'b0001; cin = 1'b1;
        #50 a = 4'b0110; b = 4'b1001; cin = 1'b0;
        #50 a = 4'b1111; b = 4'b1111; cin = 1'b1;
        #50 a = 4'b0000; b = 4'b1010; cin = 1'b0;
        #50 a = 4'b1111; b = 4'b0000; cin = 1'b0;
        #50 a = 4'b1001; b = 4'b1001; cin = 1'b0;
        #50 a = 4'b0111; b = 4'b0001; cin = 1'b1;
        */

        $finish;
    end
endmodule

/*
module tb_ripple_adder_nand;
    reg [3:0] a;
    reg [3:0] b;
    reg cin;
    wire [3:0] sum;
    wire cout;

    ripple_adder_nand dut(.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));
    integer i, j, k, l, m, n, expected_sum;
    integer a_happen, b_happen, cin_happen;
    integer a_happen2, b_happen2, cin_happen2;
    integer cur_time, max_time;

    initial begin
        //$dumpfile("ripple_adder_nand.vcd");
        //$dumpvars(0, tb_ripple_adder_nand);
        //$monitor("\na = %b, b = %b, cin = %b\nsum = %b, cout = %b", a, b, cin, sum, cout);
        max_time = 0;
        for(i = 0; i < 16; i++) begin
            for(j = 0; j < 16; j++) begin
                for(k = 0; k < 16; k++) begin
                    for(l = 0; l < 16; l++) begin
                        for(m = 0; m < 2; m++) begin
                            for(n = 0; n < 2; n++) begin
                                a = i[3:0];
                                b = j[3:0];
                                cin = m[0];
                                #50;

                                cur_time = $time;
                                a = k[3:0];
                                b = l[3:0];
                                cin = n[0];

                                expected_sum = a + b + cin;
                                wait(sum == expected_sum[3:0] && cout == expected_sum[4]);

                                if($time - cur_time > max_time) begin
                                    a_happen = k;
                                    b_happen = l;
                                    cin_happen = n;

                                    a_happen2 = i;
                                    b_happen2 = j;
                                    cin_happen2 = m;
                                    $display("%0d, %0d", $time - cur_time, max_time);
                                    max_time = $time - cur_time;
                                end
                                //$display("%0d", $time - cur_time);
                            end
                        end
                    end
                end
            end
        end

        $display("%0d ns, %0d, %0d, %0d -> %0d, %0d, %0d", max_time, a_happen2, b_happen2, cin_happen2, a_happen, b_happen, cin_happen);
        $finish;
    end
endmodule
*/
