#!/usr/bin/bash
echo "Compiling..."
iverilog -g2012 -Wall -s tb_fixed_point -o fixed_point.vvp fixed_point.v tb_fixed_point.v
echo -e "\nWriting to files..."
vvp fixed_point.vvp
echo -e "\nPlotting with python..."
python3 plot_verilog.py
echo -e "\nDone!"