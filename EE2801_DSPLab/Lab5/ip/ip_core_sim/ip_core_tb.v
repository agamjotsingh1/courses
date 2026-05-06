`timescale 1 ns / 1 ps

module ip_core_tb;

    reg clk;
    reg reset_n;

    reg signed [15:0] ast_sink_data;
    reg               ast_sink_valid;
    reg  [1:0]        ast_sink_error;

    wire signed [22:0] ast_source_data;
    wire               ast_source_valid;
    wire  [1:0]        ast_source_error;

    ip_core uut (
        .clk              (clk),
        .reset_n          (reset_n),
        .ast_sink_data    (ast_sink_data),
        .ast_sink_valid   (ast_sink_valid),
        .ast_sink_error   (ast_sink_error),
        .ast_source_data  (ast_source_data),
        .ast_source_valid (ast_source_valid),
        .ast_source_error (ast_source_error)
    );

    initial clk = 0;
    always #5 clk = ~clk; 

    reg signed [15:0] signal_mem [0:999];
    integer out_fd;

    task run_freq_test(input string in_fname, input string out_fname);
        integer fd, i, sample_int, scan_ret;
        begin
            $display("INFO: Starting test for %s", in_fname);
            
            fd = $fopen(in_fname, "r");
            out_fd = $fopen(out_fname, "w");
            
            if (fd == 0 || out_fd == 0) begin
                $display("FATAL: Could not open files for %s", in_fname);
                $finish;
            end

            for (i = 0; i < 1000; i = i + 1) begin
                scan_ret = $fscanf(fd, "%d,", sample_int); 
                signal_mem[i] = sample_int[15:0];
            end

            $fclose(fd);

            reset_n = 0;
            ast_sink_data = 16'sd0;
            ast_sink_valid = 1'b0;
            ast_sink_error = 2'b00;
            repeat(20) @(negedge clk);
            reset_n = 1;
            repeat(10) @(negedge clk);

            ast_sink_valid = 1'b1;
            for (i = 0; i < 1000; i = i + 1) begin
                ast_sink_data = signal_mem[i];
                @(negedge clk);
            end
            
            ast_sink_data = 16'sd0;
            repeat(99) @(negedge clk); 

            ast_sink_valid = 1'b0;

            repeat(150) @(negedge clk);
            
            $fclose(out_fd);
            out_fd = 0; 
            $display("INFO: Completed %s.", in_fname);
        end
    endtask

    initial begin
        run_freq_test("sig1.txt", "output_sig1.txt");
        run_freq_test("sig2.txt", "output_sig2.txt");
        run_freq_test("sig3.txt", "output_sig3.txt");
        
        $display("INFO: All frequency simulations complete.");
        $stop;
    end

    always @(posedge clk) begin
        if (ast_source_valid && out_fd != 0) begin
            $fwrite(out_fd, "%0d\n", $signed(ast_source_data));
        end
    end

endmodule
