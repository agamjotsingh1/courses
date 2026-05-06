`timescale 1ns/1ps

module assignment_1_tb;

  // Inputs for priority_encoder
  reg [3:0] in;
  wire [1:0] out;
  wire valid;

  // Inputs for up_counter
  reg clk;
  reg enable;
  reg reset;
  wire [3:0] count;

  // Inputs for even_parity_generator
  reg [7:0] data;
  wire parity;

  // Instantiate modules
  priority_encoder pe(.in(in), .out(out), .valid(valid));
  up_counter uc(.clk(clk), .count(count), .enable(enable), .reset(reset));
  even_parity_generator epg(.data(data), .parity(parity));

  // Clock generation
  initial begin
    clk = 0;
    forever #5 clk = ~clk;
  end

  // Test stimulus
  initial begin
    // VCD Dump
    $dumpfile("assignment-1.vcd");
    $dumpvars(0, assignment_1_tb);

    // Initialize inputs
    in = 4'b0000;
    enable = 0;
    reset = 1;
    data = 8'h00;

    #10;
    reset = 0;
    enable = 1;

    // Stimuli for priority encoder
    #10 in = 4'b0001;
    #10 in = 4'b0010;
    #10 in = 4'b0100;
    #10 in = 4'b1000;

    // Stimuli for parity generator
    #10 data = 8'b10101010;
    #10 data = 8'b11110000;

    // Let counter run
    #50 enable = 0;

    #50 $finish;
  end

endmodule
