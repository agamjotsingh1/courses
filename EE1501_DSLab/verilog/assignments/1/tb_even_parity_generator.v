`timescale 1ns/1ps

module tb_even_parity_generator;

    reg [7:0] data;
    wire parity;

    even_parity_generator dut (
        .data(data),
        .parity(parity)
    );

    initial begin
        $dumpfile("even_parity_generator.vcd");
        $dumpvars(0, tb_even_parity_generator);

        $display("Time\tdata\t\tparity");

        data = 8'b00000000; #10; // 0 ones => parity = 0 (even)
        $display("%0dns\t%b\t%b", $time, data, parity);

        data = 8'b00000001; #10; // 1 one => parity = 1 (odd)
        data = 8'b00000011; #10; // 2 ones => parity = 0 (even)
        data = 8'b11111111; #10; // 8 ones => parity = 0 (even)
        data = 8'b10101010; #10; // 4 ones => parity = 0
        data = 8'b11100000; #10; // 3 ones => parity = 1

        $finish;
    end
endmodule
