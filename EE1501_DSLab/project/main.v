module clock_handler (
    input clk,
    input reset,
    input set_time,
    input [7:0] input_sec,
    input [7:0] input_min,
    input [7:0] input_hour,

    output reg [7:0] current_24_sec,
    output reg [7:0] current_24_min,
    output reg [7:0] current_24_hour
);

// synchronous time set and update
always @(posedge clk or posedge reset) begin
    if (reset) begin
        current_24_sec  <= 0;
        current_24_min  <= 0;
        current_24_hour <= 0;
    end else if (set_time == 1'd1) begin
        current_24_sec  <= input_sec;
        current_24_min  <= input_min;
        current_24_hour <= input_hour;
    end else begin
        if (current_24_sec == 8'd59) begin
            current_24_sec <= 8'd0;
            if (current_24_min == 8'd59) begin
                current_24_min <= 8'd0;
                if (current_24_hour == 8'd23) begin
                    current_24_hour <= 8'd0;
                end else begin
                    current_24_hour <= current_24_hour + 1;
                end
            end else begin
                current_24_min <= current_24_min + 1;
            end
        end else begin
            current_24_sec <= current_24_sec + 1;
        end
    end
end

endmodule

module display_handler (
    input clk,
    input hour_format, // 1 for 12 hour, 0 for 24 hour format
    input timer_running,

    input [7:0] current_24_sec,
    input [7:0] current_24_min,
    input [7:0] current_24_hour,

    input [7:0] timer_min,
    input [7:0] timer_sec,

    output reg [7:0] display_sec,
    output reg [7:0] display_min,
    output reg [7:0] display_hour,
    output reg is_pm
);

// Display time in 12-hour or 24-hour format
always @(posedge clk) begin
    if(timer_running) begin
        display_sec <= timer_sec;
        display_min <= timer_min;
        display_hour <= 8'd0;

    end else begin
        display_sec <= current_24_sec;
        display_min <= current_24_min;

        if (hour_format == 1'b1) begin  // 12-hour format
            if (current_24_hour == 0) begin
                display_hour <= 8'd12;  // 12 AM (midnight)
            end else if (current_24_hour == 12) begin
                display_hour <= 8'd12;  // 12 PM (noon)
            end else if (current_24_hour > 12) begin
                display_hour <= current_24_hour - 12;  // PM hours
            end else begin
                display_hour <= current_24_hour;  // AM hours
            end
        end else begin  // 24-hour format
            display_hour <= current_24_hour;
        end

        if (hour_format == 1'b1) begin  // 12-hour format
            is_pm <= (current_24_hour >= 12) ? 1'b1 : 1'b0;
        end else begin
            is_pm <= 1'b0;  // Don't care in 24-hour mode
        end
    end
end

endmodule

module date_handler (
    input clk,
    input reset,
    input set_date,
    input [7:0] input_day,
    input [7:0] input_month,
    input [15:0] input_year,

    // Clock time inputs to detect day changes
    input [7:0] current_24_hour,
    input [7:0] current_24_min,
    input [7:0] current_24_sec,

    // Date outputs
    output reg [ 7:0] current_day,
    output reg [ 7:0] current_month,
    output reg [15:0] current_year
);

// Internal signals
reg [7:0] days_in_current_month;

// Date handling logic
always @(posedge clk or posedge reset) begin
    if (reset) begin
        // Reset to default date
        current_day   <= 8'd1;
        current_month <= 8'd1;
        current_year  <= 16'd2020;

    end else if (set_date) begin
        // Set date manually when set_date is active
        current_day   <= input_day;
        current_month <= input_month;
        current_year  <= input_year;

    end else if (current_24_hour == 8'd23 && current_24_min == 8'd59 && current_24_sec == 8'd59) begin
        // Day changes at midnight (23:59:59)

        // First determine days in current month without using a function
        case (current_month)
            8'd1, 8'd3, 8'd5, 8'd7, 8'd8, 8'd10, 8'd12:
                days_in_current_month = 8'd31;  // Jan, Mar, May, Jul, Aug, Oct, Dec

            8'd4, 8'd6, 8'd9, 8'd11: days_in_current_month = 8'd30;  // Apr, Jun, Sep, Nov

            8'd2: begin  // February
                // Check leap year
                if (((current_year % 4 == 0) && (current_year % 100 != 0)) || (current_year % 400 == 0))
                    days_in_current_month = 8'd29;  // Leap year
                else days_in_current_month = 8'd28;  // Non-leap year
            end

            default: days_in_current_month = 8'd30;  // Default case
        endcase

        // Update date
        if (current_day == days_in_current_month) begin
            current_day <= 8'd1;  // Reset day to 1

            if (current_month == 8'd12) begin
                current_month <= 8'd1;  // Reset month to January
                current_year  <= current_year + 16'd1;  // Increment year
            end else begin
                current_month <= current_month + 8'd1;  // Increment month
            end
        end else begin
            current_day <= current_day + 8'd1;  // Increment day
        end
    end
end

endmodule

module alarm_handler (
    input clk,
    input set_alarm,

    input [7:0] current_24_sec,
    input [7:0] current_24_min,
    input [7:0] current_24_hour,

    input [7:0] alarm_input_sec,
    input [7:0] alarm_input_min,
    input [7:0] alarm_input_hour,

    input snooze_alarm,
    input stop_alarm,

    output reg alarm_buzzer
);
    reg [7:0] input_sec_internal;
    reg [7:0] input_min_internal;
    reg [7:0] input_hour_internal;
    reg [9:0] counter;
    reg is_snoozed;
    reg is_buzzing;

always @(posedge clk) begin
    // Stop alarm functionality
    if(stop_alarm) begin
        is_buzzing <= 0;
        alarm_buzzer <= 0;
        counter <= 0;
    end
    // Snooze alarm functionality
    else if(snooze_alarm) begin
        is_snoozed <= 1;
        alarm_buzzer <= 0;
        is_buzzing <= 0;
        counter <= 0;
    end
    // Set alarm functionality
    else if(set_alarm) begin
        input_sec_internal <= alarm_input_sec;
        input_min_internal <= alarm_input_min;
        input_hour_internal <= alarm_input_hour;
        is_snoozed <= 0;
        alarm_buzzer <= 0;
        is_buzzing <= 0;
        counter <= 0;
    end
    // Snooze timer functionality
    else if(is_snoozed) begin
        alarm_buzzer <= 0;
        is_buzzing <= 0;
        counter <= counter + 1;
        if(counter >= 5) begin  // After snooze period (300 clock cycles)
            is_snoozed <= 0;
            alarm_buzzer <= 1;
            is_buzzing <= 1;
            counter <= 0;
        end
    end
    // Alarm matching current time
    else if ((input_sec_internal == current_24_sec &&
              input_min_internal == current_24_min &&
              input_hour_internal == current_24_hour) || is_buzzing) begin
        if(!is_buzzing) is_buzzing <= 1;
        alarm_buzzer <= 1;
    end
    // Default state - alarm not active
    else begin
        alarm_buzzer <= 0;
    end
end

endmodule

module timer_handler (
    input clk,
    input reset,
    input start_timer,
    input stop_timer,
    input set_timer,
    input [7:0] input_min,
    input [7:0] input_sec,

    output reg [7:0] timer_min,
    output reg [7:0] timer_sec,
    output reg timer_running,
    output reg timer_buzzer
);

reg [7:0] max_min = 8'd10;

always @(posedge clk or posedge reset) begin
    if (reset) begin
        timer_min <= 8'd0;
        timer_sec <= 8'd0;
        timer_running <= 1'b0;
        timer_buzzer <= 1'b0;
    end else if (set_timer) begin
        if (input_min > max_min) begin
            // Limit to maximum 10 minutes
            timer_min <= max_min;
            timer_sec <= input_sec;
        end else begin
            timer_min <= input_min;
            timer_sec <= input_sec;
        end
        timer_running <= 1'b0;
        timer_buzzer <= 1'b0;
    end else if (start_timer) begin
        timer_running <= 1'b1;
        timer_buzzer <= 1'b0;
    end else if (stop_timer) begin
        // Stop the timer
        timer_running <= 1'b0;
        timer_buzzer <= 1'b0;
    end

    if (timer_running) begin
        // Timer is running, decrement
        if (timer_sec == 8'd0) begin
            if (timer_min == 8'd0) begin
                // Timer has reached zero
                timer_running <= 1'b0;
                timer_buzzer <= 1'b1;
            end else begin
                // Decrement minute, reset seconds to 59
                timer_min <= timer_min - 8'd1;
                timer_sec <= 8'd59;
            end
        end else begin
            // Decrement seconds
            timer_sec <= timer_sec - 8'd1;
        end
    end
end

endmodule

module main_driver (
    input        clk,
    input        reset,
    input        hour_format,
    input        set_time,
    input        set_date,
    input        set_alarm,
    input        snooze_alarm,
    input        stop_alarm,
    input        set_timer,
    input        start_timer,
    input        stop_timer,

    input  [7:0] input_sec,
    input  [7:0] input_min,
    input  [7:0] input_hour,
    input  [7:0] input_day,
    input  [7:0] input_month,
    input [15:0] input_year,
    input  [7:0] timer_input_min,
    input  [7:0] timer_input_sec,
    input  [7:0] alarm_input_sec,
    input  [7:0] alarm_input_min,
    input  [7:0] alarm_input_hour,

    output [7:0] current_24_sec,
    output [7:0] current_24_min,
    output [7:0] current_24_hour,
    output [7:0] display_sec,
    output [7:0] display_min,
    output [7:0] display_hour,
    output [7:0] current_day,
    output [7:0] current_month,
    output [15:0] current_year,
    output [7:0] timer_min,
    output [7:0] timer_sec,
    output       timer_running,
    output       timer_buzzer,
    output       alarm_buzzer,
    output       is_pm
);
    // Instantiate the clock_handler module
    clock_handler clock_module (
        .clk(clk),
        .reset(reset),
        .set_time(set_time),
        .input_sec(input_sec),
        .input_min(input_min),
        .input_hour(input_hour),
        .current_24_sec(current_24_sec),
        .current_24_min(current_24_min),
        .current_24_hour(current_24_hour)
    );

    // Instantiate the display_handler module
    display_handler display_module (
        .clk(clk),
        .hour_format(hour_format),
        .current_24_sec(current_24_sec),
        .current_24_min(current_24_min),
        .current_24_hour(current_24_hour),
        .timer_min(timer_min),
        .timer_sec(timer_sec),
        .timer_running(timer_running),
        .display_sec(display_sec),
        .display_min(display_min),
        .display_hour(display_hour),
        .is_pm(is_pm)
    );

    // Instantiate the date_handler module
    date_handler date_module (
        .clk(clk),
        .reset(reset),
        .set_date(set_date),
        .input_day(input_day),
        .input_month(input_month),
        .input_year(input_year),
        .current_24_hour(current_24_hour),
        .current_24_min(current_24_min),
        .current_24_sec(current_24_sec),
        .current_day(current_day),
        .current_month(current_month),
        .current_year(current_year)
    );

    // Instantiate the timer_handler module
    timer_handler timer_module (
        .clk(clk),
        .reset(reset),
        .set_timer(set_timer),
        .start_timer(start_timer),
        .stop_timer(stop_timer),
        .input_min(timer_input_min),
        .input_sec(timer_input_sec),
        .timer_min(timer_min),
        .timer_sec(timer_sec),
        .timer_running(timer_running),
        .timer_buzzer(timer_buzzer)
    );

    // Instantiate the alarm_handler module
    alarm_handler alarm_module (
        .clk(clk),
        .set_alarm(set_alarm),
        .snooze_alarm(snooze_alarm),
        .stop_alarm(stop_alarm),
        .current_24_hour(current_24_hour),
        .current_24_min(current_24_min),
        .current_24_sec(current_24_sec),
        .alarm_input_sec(alarm_input_sec),
        .alarm_input_min(alarm_input_min),
        .alarm_input_hour(alarm_input_hour),
        .alarm_buzzer(alarm_buzzer)
    );
endmodule
