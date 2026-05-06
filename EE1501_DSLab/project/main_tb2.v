`timescale 1s/1ms

module clock_tb;
    // Inputs
    reg clk;
    reg reset;
    reg hour_format;
    reg set_time;
    reg set_date;
    reg set_alarm;
    reg snooze_alarm;
    reg stop_alarm;
    reg set_timer;
    reg start_timer;
    reg stop_timer;
    
    reg [7:0] input_sec;
    reg [7:0] input_min;
    reg [7:0] input_hour;
    reg [7:0] input_day;
    reg [7:0] input_month;
    reg [15:0] input_year;
    reg [7:0] timer_input_min;
    reg [7:0] timer_input_sec;
    reg [7:0] alarm_input_sec;
    reg [7:0] alarm_input_min;
    reg [7:0] alarm_input_hour;
    
    // Outputs
    wire [7:0] current_24_sec;
    wire [7:0] current_24_min;
    wire [7:0] current_24_hour;
    wire [7:0] display_sec;
    wire [7:0] display_min;
    wire [7:0] display_hour;
    wire [7:0] current_day;
    wire [7:0] current_month;
    wire [15:0] current_year;
    wire [7:0] timer_min;
    wire [7:0] timer_sec;
    wire timer_running;
    wire timer_buzzer;
    wire alarm_buzzer;
    
    // Instantiating the main driver for the clock
    main_driver dut (
        .clk(clk),
        .reset(reset),
        .hour_format(hour_format),
        .set_time(set_time),
        .set_date(set_date),
        .set_alarm(set_alarm),
        .snooze_alarm(snooze_alarm),
        .stop_alarm(stop_alarm),
        .set_timer(set_timer),
        .start_timer(start_timer),
        .stop_timer(stop_timer),
        .input_sec(input_sec),
        .input_min(input_min),
        .input_hour(input_hour),
        .input_day(input_day),
        .input_month(input_month),
        .input_year(input_year),
        .timer_input_min(timer_input_min),
        .timer_input_sec(timer_input_sec),
        .alarm_input_sec(alarm_input_sec),
        .alarm_input_min(alarm_input_min),
        .alarm_input_hour(alarm_input_hour),
        .current_24_sec(current_24_sec),
        .current_24_min(current_24_min),
        .current_24_hour(current_24_hour),
        .display_sec(display_sec),
        .display_min(display_min),
        .display_hour(display_hour),
        .current_day(current_day),
        .current_month(current_month),
        .current_year(current_year),
        .timer_min(timer_min),
        .timer_sec(timer_sec),
        .timer_running(timer_running),
        .timer_buzzer(timer_buzzer),
        .alarm_buzzer(alarm_buzzer)
    );
    
    // AM/PM indicator logic
    reg is_pm;
    reg [15:0] am_pm_indicator;
    
    // Display logic for AM/PM indicator
    always @(*) begin
        is_pm = (current_24_hour >= 8'd12);
        
        if (hour_format) begin
            if (is_pm)
                am_pm_indicator = {"P", "M"};  // 'P' = 8'h50, 'M' = 8'h4D
            else
                am_pm_indicator = {"A", "M"};  // 'A' = 8'h41, 'M' = 8'h4D
        end else begin
            am_pm_indicator = "  ";  // Two spaces if 24-hour
        end
    end
    
    // Clock generation (1 Hz clock for seconds)
    initial begin
        clk = 0;
        forever #0.5 clk = ~clk;  // 1 second period
    end
    
    // Test sequence
    initial begin
        // Initialize all inputs
        reset = 0;
        hour_format = 0;  // 24-hour mode
        set_time = 0;
        set_date = 0;
        set_alarm = 0;
        snooze_alarm = 0;
        stop_alarm = 0;
        set_timer = 0;
        start_timer = 0;
        stop_timer = 0;
        
        input_sec = 0;
        input_min = 0;
        input_hour = 0;
        input_day = 0;
        input_month = 0;
        input_year = 0;
        timer_input_min = 0;
        timer_input_sec = 0;
        alarm_input_sec = 0;
        alarm_input_min = 0;
        alarm_input_hour = 0;
        
        // First reset
        #1 reset = 1;
        #2 reset = 0;
        $display("Reset done at %0ds", $time);
        
        // Set date to Dec 31 2022, time to 23:53:55
        input_day = 8'd31;
        input_month = 8'd12;
        input_year = 16'd2022;
        #1 set_date = 1;
        #1 set_date = 0;
        
        input_hour = 8'd23;
        input_min = 8'd59;
        input_sec = 8'd58;
        #1 set_time = 1;
        $display("Set date to Dec 31 2022, time to 23:59:58 at %0ds", $time);
        #1 set_time = 0;
        
        $display("Waiting for next day to start...");
        #2;
        $display("Next day started at %0ds", $time);
        
        // Change to AM-PM mode
        #1 hour_format = 1;
        $display("Changed to AM-PM mode at %0ds", $time);
        
        // Wait for 10 seconds
        #10;
        
        // Change date to Feb 28 2020 and time to 23:53:55
        input_day = 8'd28;
        input_month = 8'd2;
        input_year = 16'd2020;
        #1 set_date = 1;
        #1 set_date = 0;
        
        input_hour = 8'd23;
        input_min = 8'd59;
        input_sec = 8'd57;
        #1 set_time = 1;
        $display("Set date to Feb 28 2020, time to 23:59:57 at %0ds", $time);
        #1 set_time = 0;
        
        $display("Waiting for next day to start...");
        #4;
        $display("Next day started at %0ds", $time);
        // Wait 10 seconds
        hour_format = 0;
        $display("Change to 24-Hour format");
        #10;

        // Set an alarm for 00:00:30
        $display("Set alarm for 00:00:30 at %0ds", $time);
        alarm_input_hour = 8'd0;
        alarm_input_min = 8'd0;
        alarm_input_sec = 8'd30;
        #1 set_alarm = 1;
        #1 set_alarm = 0;
        
        // Wait for alarm to trigger (should be in about 20 seconds)
        wait(alarm_buzzer);
        $display("Alarm triggered at %0ds", $time);
        
        // Snooze
        #5 snooze_alarm = 1;
        #2 snooze_alarm = 0;
        $display("Alarm snoozed at %0ds", $time);
        
        // Wait 5 seconds and stop alarm
        #5;
        #2 stop_alarm = 1;
        $display("Alarm stopped at %0ds", $time);
        #2 stop_alarm = 0;
        
        // Set a timer for 1 minute (60 seconds)
        timer_input_min = 8'd0;
        timer_input_sec = 8'd2;
        #1 set_timer = 1;
        #1 set_timer = 0;
        #1 start_timer = 1;
        #1 start_timer = 0;
        $display("Set timer for 2 seconds at %0ds", $time);
        
        #5 stop_timer = 1;
        // End simulation
        #1 $finish;
    end
    
    // Monitor the clock outputs
    initial begin
        $monitor("Time: %0ds, Date: %0d/%0d/%0d, Time: %0d:%0d:%0d %s, Alarm: %b, Timer: %b",
                 $time,
                 current_day, current_month, current_year,
                 display_hour, display_min, display_sec,
                 am_pm_indicator,
                 alarm_buzzer,
                 timer_buzzer);
    end
       initial begin
       $dumpfile("wave.vcd");
       $dumpvars(0, clock_tb);
   end
endmodule
