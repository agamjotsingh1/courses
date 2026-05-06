`timescale 1ns/1ns

module ripple_adder_nand (
    input [3:0] a,
    input [3:0] b,
    input cin,
    output [3:0] sum,
    output cout
);
    wire cout1, cout2, cout3;
    full_adder_nand adder1(.a(a[0]), .b(b[0]), .cin(cin), .sum(sum[0]), .cout(cout1));
    full_adder_nand adder2(.a(a[1]), .b(b[1]), .cin(cout1), .sum(sum[1]), .cout(cout2));
    full_adder_nand adder3(.a(a[2]), .b(b[2]), .cin(cout2), .sum(sum[2]), .cout(cout3));
    full_adder_nand adder4(.a(a[3]), .b(b[3]), .cin(cout3), .sum(sum[3]), .cout(cout));
endmodule

module full_adder_nand (
    input a,
    input b,
    input cin,
    output sum,
    output cout
);

    // sum = a ^ b ^ cin;
    wire ab_xor;

    xor_nand xor_gate1(a, b, ab_xor);
    xor_nand xor_gate2(ab_xor, cin, sum);

    // carry (cout) = a & b | cin & a | cin & b;
    wire and1, and2, and3, or1;

    and_nand and_gate1(a, b, and1);
    and_nand and_gate2(cin, a, and2);
    and_nand and_gate3(cin, b, and3);
    or_nand or_gate1(and1, and2, or1);
    or_nand or_gate2(and3, or1, cout);
endmodule

module xor_nand (
    input a,
    input b,
    output out
);
    wire ab_nand, a_ab_nand, b_ab_nand;
    nand #1(ab_nand, a, b);
    nand #1(a_ab_nand, ab_nand, a);
    nand #1(b_ab_nand, ab_nand, b);
    nand #1(out, a_ab_nand, b_ab_nand);
endmodule

module and_nand (
    input a,
    input b,
    output out
);
    wire ab_nand;
    nand #1(ab_nand, a, b);
    nand #1(out, ab_nand, ab_nand); // basically not of nand
endmodule

module or_nand (
    input a,
    input b,
    output out
);
    wire ab_nand, a_not, b_not;
    nand #1(a_not, a, a); // not gate
    nand #1(b_not, b, b); // not gate
    nand #1(out, a_not, b_not);
endmodule
