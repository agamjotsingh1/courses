#!/bin/bash
set -e

UTILS=(
    util/*.v
)

# echo "[1/4] Running Python Generation Script..."
# python3 fir_generate.py
# echo " -> Coeffs and test signals generated."

echo ""
echo "[1/3] Compiling and running Direct FIR..."
iverilog -g2012 -o ./sims/direct.vvp ./direct/tb_fir_direct.v ./direct/fir_direct.v "${UTILS[@]}"
vvp ./sims/direct.vvp
echo " -> Direct test completed."

# echo ""
# echo "[2/3] Compiling and running Direct 2 FIR..."
# iverilog -g2012 -o ./sims/direct_2.vvp ./direct_2/tb_fir_direct.v ./direct_2/fir_direct.v "${UTILS[@]}"
# vvp ./sims/symmetric.vvp
# echo " -> Direct test 2 completed."

# echo ""
# echo "[2/3] Compiling and running Symmetric FIR..."
# iverilog -g2012 -o ./sims/symmetric.vvp ./symmetric/tb_fir_symmetric.v ./symmetric/fir_symmetric.v "${UTILS[@]}"
# vvp ./sims/symmetric.vvp
# echo " -> Symmetric test completed."



# echo ""
# echo "[3/3] Compiling and running Genvar FIR..."
# iverilog -g2012 -o ./sims/genvar.vvp ./genvar/tb_fir_genvar.v ./genvar/fir_genvar.v "${UTILS[@]}"
# vvp ./sims/genvar.vvp
# echo " -> Genvar Form test completed."