#!/bin/bash
set -e

python3 gen_sigs.py
python3 gen_twiddles.py

echo ""
echo ">>> Compiling and running FFT verilog sim..."
SRCS=$(ls *.v | grep -v '^tb_')
iverilog -g2012 -o fft.vvp tb_fft.v $SRCS
vvp fft.vvp
echo " -> Verilog FFT sim completed. Output signals generated"