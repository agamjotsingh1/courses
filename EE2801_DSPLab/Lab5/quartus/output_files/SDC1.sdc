# 1. Create the base clock
# Replace 'clk' with the exact name of your top-level clock input port
# Replace '50.0' with your actual physical board clock frequency in MHz
# The '-period 20.0' is the period in nanoseconds (1 / 50MHz = 20ns)
create_clock -name {sys_clk} -period 20 [get_ports {clk}]

# 2. Derive clock uncertainty
# This is an Altera/Intel specific command. It automatically calculates 
# internal clock jitter, skew, and other safe margins. ALWAYS include this.
derive_clock_uncertainty

# 3. Derive PLL clocks (Optional but highly recommended)
# If your design uses a Phase-Locked Loop (PLL) IP core to generate other clocks,
# this command automatically finds them and constrains them based on your PLL settings.
derive_pll_clocks