#!/usr/bin/bash
set -e

echo "Generating config files for verilog..."
python3 divider/gens/configgen.py

echo "Generating LUT..."
python3 divider/gens/lutgen.py

FILES=(
    config.vh
    divider/*.v
    util/*.v
)

echo -e "\nCompiling verilog..."
iverilog -g2012 -Wall -s tb_divider -o divider.vvp "${FILES[@]}" tb_divider.v

echo -e "\nGenerating test files..."
python3 testing/testsgen.py

echo -e "\nExecuting testbench..."
vvp divider.vvp

echo -e "\nChecking verilog results with python...\n"
python3 testing/check.py

echo -e "\nDone!"