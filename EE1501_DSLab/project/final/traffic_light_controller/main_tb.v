`timescale 1s/1ms

module tb_traffic_light_controller;

    reg clk, reset;
    reg Emergency_Left, Emergency_Right;
    wire [1:0] T1, T2;
    wire T1_WALK, T2_WALK, buzzer1, buzzer2;

    // Instantiate your module
    traffic_light_controller uut (
        .clk(clk),
        .reset(reset),
        .Emergency_Left(Emergency_Left),
        .Emergency_Right(Emergency_Right),
        .T1(T1),
        .T2(T2),
        .T1_WALK(T1_WALK),
        .T2_WALK(T2_WALK),
        .buzzer1(buzzer1),
        .buzzer2(buzzer2)
    );

    // Clock generation
    initial begin
        clk = 0;
        forever #0.5 clk = ~clk;
    end

    // Light name string variables (for display)
    reg [8*6:1] T1_str, T2_str;

    always @* begin
        case (T1)
            2'b00: T1_str = "GREEN ";
            2'b01: T1_str = "YELLOW";
            2'b10: T1_str = "RED   ";
            default: T1_str = "UNKWN ";
        endcase

        case (T2)
            2'b00: T2_str = "GREEN ";
            2'b01: T2_str = "YELLOW";
            2'b10: T2_str = "RED   ";
            default: T2_str = "UNKWN ";
        endcase
    end

    // Print when anything changes
    initial begin
        $monitor("Time: %0d | T1: %s | T2: %s | T1_WALK = %b | T2_WALK = %b | Buzzer1 = %b | Buzzer2 = %b | E_Left = %b | E_Right = %b",
                 $time, T1_str, T2_str, T1_WALK, T2_WALK, buzzer1, buzzer2, Emergency_Left, Emergency_Right);
    end

    // Stimulus
    integer i;
    initial begin
        // Start VCD file generation
        $dumpfile("wave.vcd");
        $dumpvars(0, tb_traffic_light_controller);
        
        $display("\n=== T-Junction Traffic Light Controller Simulation Started ===\n");

        Emergency_Left = 0;
        Emergency_Right = 0;
        reset = 1;
        #1;
        reset = 0;
        $display("=== Reset at t=%0d ===", $time);

        // Normal operation - let it go through a complete cycle
        $display("\n=== Normal Operation - Full Cycle ===");
        #100;

        // Test Case 1: Short Emergency Left (< T_EM)
        $display("\n=== Test Case 1: Short Emergency Left (<T_EM) ===");
        Emergency_Left = 1;
        #2;
        Emergency_Left = 0;
        // Wait for emergency to complete (should be T_EM = 9 seconds)
        #15;

        // Test Case 2: Long Emergency Left (> T_EM)
        $display("\n=== Test Case 2: Long Emergency Left (>T_EM) ===");
        Emergency_Left = 1;
        #15;
        Emergency_Left = 0;
        // Wait for emergency to complete
        #15;

        // Test Case 3: Short Emergency Right (< T_EM)
        $display("\n=== Test Case 3: Short Emergency Right (<T_EM) ===");
        Emergency_Right = 1;
        #2;
        Emergency_Right = 0;
        // Wait for emergency to complete (should be T_EM = 9 seconds)
        #15;

        // Test Case 4: Long Emergency Right (> T_EM)
        $display("\n=== Test Case 4: Long Emergency Right (>T_EM) ===");
        Emergency_Right = 1;
        #15;
        Emergency_Right = 0;
        // Wait for emergency to complete
        #15;

        // Test Case 5: Priority test - Both emergencies active, Right should take priority
        $display("\n=== Test Case 5: Priority Test - Both Emergencies Active ===");
        Emergency_Left = 1;
        Emergency_Right = 1;
        #15;
        Emergency_Right = 0;
        #5;
        Emergency_Left = 0;
        // Wait for emergency to complete
        #15;

        // Test Case 6: Overlapping emergencies - Left starts, then Right interrupts
        $display("\n=== Test Case 6: Overlapping Emergencies - Left then Right ===");
        Emergency_Left = 1;
        #5;
        Emergency_Right = 1;
        #5;
        Emergency_Left = 0;
        #5;
        Emergency_Right = 0;
        // Wait for emergency to complete
        #15;

        // Test Case 7: Overlapping emergencies - Right starts, then Left (should be ignored until Right is done)
        $display("\n=== Test Case 7: Overlapping Emergencies - Right then Left ===");
        Emergency_Right = 1;
        #5;
        Emergency_Left = 1;
        #5;
        Emergency_Right = 0;
        #5;
        Emergency_Left = 0;
        // Wait for emergency to complete
        #15;

        // Test Case 8: Back-to-back emergencies
        $display("\n=== Test Case 8: Back-to-back Emergencies ===");
        Emergency_Right = 1;
        #5;
        Emergency_Right = 0;
        #12; // Just after first emergency ends
        Emergency_Left = 1;
        #5;
        Emergency_Left = 0;
        // Wait for emergency to complete
        #15;

        // Final normal operation
        $display("\n=== Final Normal Operation ===");
        #50;

        $display("\n=== Simulation Complete ===\n");
        $finish;
    end

endmodule
