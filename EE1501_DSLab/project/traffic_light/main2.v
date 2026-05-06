`timescale 1s/1ms

// traffic_light_controller.v
module traffic_light_controller(
    input            clk,
    input            reset,
    input            Emergency_Left,
    input            Emergency_Right,
    output reg [1:0] T1,        // 00:G, 01:Y, 10:R
    output reg [1:0] T2,        // 00:G, 01:Y, 10:R
    output reg       T1_WALK,
    output reg       T2_WALK,
    output reg       buzzer
);

    // State encoding
    localparam S1 = 3'd1,
               S2 = 3'd2,
               S3 = 3'd3,
               S4 = 3'd4,
               S5 = 3'd5,
               S6 = 3'd6;

    // Timing constants (in clock ticks)
    localparam T_S1 = 29,
               T_S2 =  4,
               T_S3 = 19,
               T_S4 =  4,
               T_S5 =  29,
               T_S6 = 4,
               T_EM =  9;

    reg [2:0] current_state, next_state;
    reg [6:0] timer, emergency_timer;

    // State register + outputs reset
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            current_state   <= S1;
            timer           <= 0;
            emergency_timer <= 0;
            T1       <= 2'b00;
            T2       <= 2'b10;
            T1_WALK  <= 1'b0;
            T2_WALK  <= 1'b0;
            buzzer   <= 1'b0;
        end else begin
            // ----- Emergency priority -----
            case (Emergency_Left | Emergency_Right)
              1'b1: begin
                // first, check Left
                case (Emergency_Right)
                  1'b1: begin
                    case (emergency_timer < T_EM)
                      1'b1:    emergency_timer <= emergency_timer + 1;
                      default: begin
                                 emergency_timer <= 0;
                                 current_state   <= next_state;
                               end
                    endcase
                    T1       <= 2'b10;
                    T2       <= 2'b10;
                    T1_WALK  <= 1'b0;
                    T2_WALK  <= 1'b0;
                    buzzer   <= 1'b0;
                  end
                  default: begin
                    // then, if not Left, check Right
                    case (Emergency_Left)
                      1'b1: begin
                        case (emergency_timer < T_EM)
                          1'b1:    emergency_timer <= emergency_timer + 1;
                          default: begin
                                     emergency_timer <= 0;
                                     // current_state   <= next_state;
                                   end
                        endcase
                        T1       <= 2'b10;
                        T2       <= 2'b00;
                        T1_WALK  <= 1'b0;
                        T2_WALK  <= 1'b0;
                        buzzer   <= 1'b0;
                      end
                    endcase
                  end
                endcase
              end

              // ----- Normal operation -----
              default: begin
                case (current_state)
                  S1: begin
                    T1_WALK <= 1'b0; T2_WALK <= 1'b0; buzzer <= 1'b0;
                    T1      <= 2'b00; T2      <= 2'b10;
                    if (timer < T_S1)
                      timer <= timer + 1;
                    else begin
                      timer         <= 0;
                      current_state <= S2;
                    end
                  end
                  S2: begin
                    T1_WALK <= 1'b0; T2_WALK <= 1'b0; buzzer <= 1'b0;
                    T1      <= 2'b01; T2      <= 2'b10;
                    if (timer < T_S2)
                      timer <= timer + 1;
                    else begin
                      timer         <= 0;
                      current_state <= S3;
                    end
                  end
                  S3: begin
                    T1_WALK <= 1'b1; T2_WALK <= 1'b1; buzzer <= 1'b0;
                    T1      <= 2'b10; T2      <= 2'b10;
                    if (timer < T_S3)
                      timer <= timer + 1;
                    else begin
                      timer         <= 0;
                      current_state <= S4;
                    end
                  end
                  S4: begin
                    T1_WALK <= 1'b1; T2_WALK <= 1'b1; buzzer <= 1'b1;
                    T1      <= 2'b10; T2      <= 2'b10;
                    if (timer < T_S4)
                      timer <= timer + 1;
                    else begin
                      timer         <= 0;
                      current_state <= S5;
                    end
                  end
                  S5: begin
                    T1_WALK <= 1'b0; T2_WALK <= 1'b0; buzzer <= 1'b0;
                    T1      <= 2'b10; T2      <= 2'b00;
                    if (timer < T_S5)
                      timer <= timer + 1;
                    else begin
                      timer         <= 0;
                      current_state <= S6;
                    end
                  end
                  S6: begin
                    T1_WALK <= 1'b0; T2_WALK <= 1'b0; buzzer <= 1'b0;
                    T1      <= 2'b10; T2      <= 2'b01;
                    if (timer < T_S6)
                      timer <= timer + 1;
                    else begin
                      timer         <= 0;
                      current_state <= S1;
                    end
                  end
                  default: current_state <= S1;
                endcase
              end
            endcase
        end
    end

    // Next-state logic (unchanged)
    always @(*) begin
        case (current_state)
            S1: next_state = S2;
            S2: next_state = S3;
            S3: next_state = S4;
            S4: next_state = S5;
            S5: next_state = S6;
            S6: next_state = S1;
            default: next_state = S1;
        endcase
    end

endmodule
