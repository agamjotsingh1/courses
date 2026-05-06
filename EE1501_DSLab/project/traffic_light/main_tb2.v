`timescale 1s / 1ms

module traffic_light_controller_tb;

    // Inputs
    reg clk;
    reg reset;
    reg Emergency_Left;
    reg Emergency_Right;

    // Outputs
    wire [1:0] T1;
    wire [1:0] T2;
    wire T1_WALK;
    wire T2_WALK;
    wire buzzer;

    // Internal readable signals
    reg [8*6:1] T1_str;
    reg [8*6:1] T2_str;

    // Instantiate DUT
    traffic_light_controller uut (
        .clk(clk),
        .reset(reset),
        .Emergency_Left(Emergency_Left),
        .Emergency_Right(Emergency_Right),
        .T1(T1),
        .T2(T2),
        .T1_WALK(T1_WALK),
        .T2_WALK(T2_WALK),
        .buzzer(buzzer)
    );

    // Clock generation
    always #0.5 clk = ~clk; // 1s period

    // Convert T1 and T2 codes to strings
    always @(*) begin
        case (T1)
            2'b00: T1_str = "G";
            2'b01: T1_str = "Y";
            2'b10: T1_str = "R";
            default: T1_str = "UNDEF";
        endcase

        case (T2)
            2'b00: T2_str = "G";
            2'b01: T2_str = "Y";
            2'b10: T2_str = "R";
            default: T2_str = "UNDEF";
        endcase
    end

    initial begin
        $dumpfile("traffic_light_controller.vcd");
        $dumpvars(0, traffic_light_controller_tb);
        
        $display("=== Starting Full Testbench ===");
        $display("Time\tT1 T2 T1_WALK T2_WALK Buzzer E_Left E_Right");

        $monitor("%0d\t%s %s %b %b %b %b %b",
                 $time, T1_str, T2_str,
                 T1_WALK, T2_WALK, buzzer,
                 Emergency_Left, Emergency_Right);

        clk = 0;
        reset = 1;
        Emergency_Left = 0;
        Emergency_Right = 0;

        #20 reset = 0;

        // === NORMAL STATE SEQUENCE TEST ===
        // Total time through full FSM: S1 (30s) + S2 (5s) + S3 (35s) + S4 (20s) + S5 (30s) + S6 (5s) + S7 (30s) = 155s
        // Each second = 1000ns = 100 clock cycles (since clk = 10ns)

        #155; // Wait full cycle

        // === RESET TEST ===
        $display("\n[Time %0d] >>> Applying Reset <<<", $time);
        reset = 1;
        #20;
        reset = 0;

        #2;

        // === EMERGENCY LEFT IN S1 ===
        $display("\n[Time %0d] >>> Emergency Left Triggered in S1 <<<", $time);
        Emergency_Left = 1;
        #10;
        Emergency_Left = 0;
        #5;

        // === EMERGENCY RIGHT IN S3 (PEDESTRIAN) ===
        $display("\n[Time %0d] >>> Emergency Right Triggered in S3 <<<", $time);
        #30; // Enter S3 manually
        Emergency_Right = 1;
        #10;
        Emergency_Right = 0;
        #50;

        // === BUZZER BEHAVIOR TEST IN S3 AND S4 ===
        // S3 buzzer triggers at t = 30s to 35s => 5s duration
        // S4 buzzer triggers in first 5s

        $display("\n[Time %0d] >>> Waiting for buzzer in S3 & S4 <<<", $time);
        #35; // Enough to enter and finish both S3 and S4

        // === EMERGENCY RIGHT IN S6 ===
        $display("\n[Time %0d] >>> Emergency Right Triggered in S6 <<<", $time);
        #60;
        Emergency_Right = 1;
        #10;
        Emergency_Right = 0;

        // === FINAL STATE LOOP TEST ===
        $display("\n[Time %0d] >>> Letting FSM loop again <<<", $time);
        #160;

        $display("=== Testbench Complete ===");
        $finish;
    end

endmodule

