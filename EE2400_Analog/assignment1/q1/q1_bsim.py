import numpy as np
from scipy.optimize import fsolve

# --- 1. HARCODED VALUES FROM YOUR MODEL CARD ---
Vdd   = 3.3
Rl    = 10000        # 10k resistor
W     = 1e-6         # From your schematic
L     = 1e-6         # From your schematic
tox   = 4.1e-9       # From your model card
vth0  = 0.3662473    # From your model card
u0    = 273.8 * 1e-4 # cm^2/Vs -> m^2/Vs
vsat  = 1.355e5      # Velocity Saturation
pclm  = 1.3822       # Channel Length Modulation
eta0  = 2.23e-3      # DIBL factor

# --- 2. PHYSICS CONSTANTS ---
eps_ox = 3.9 * 8.854e-12
cox    = eps_ox / tox

def solve_exact(vars):
    vgs, vds = vars
    
    # Threshold with DIBL (Drain-Induced Barrier Lowering)
    vth = vth0 - eta0 * vds
    vgt = vgs - vth
    if vgt < 0: vgt = 1e-9
    
    # Velocity Saturation effect (Why Level 1 math fails)
    esat = 2 * vsat / u0
    vdsat = (esat * L * vgt) / (esat * L + vgt)
    
    # Saturation Current with CLM (The "Slope")
    beta = u0 * cox * (W / L)
    id_base = beta * (vgt**2) / (2 * (1 + vgt / (esat * L)))
    
    # PCLM is logarithmic in BSIM3, not a simple linear (1 + lambda*Vds)
    clm_factor = 1 + pclm * np.log(1 + (max(0, vds - vdsat)) / L)
    id_final = id_base * clm_factor

    # --- THE TWO EQUATIONS ---
    # Eq 1: Your design constraint
    eq1 = vds - (Vdd + vgs - vth) / 2
    
    # Eq 2: Circuit Physics (KVL)
    eq2 = vds - (Vdd - id_final * Rl)
    
    return [eq1, eq2]

vgs_sol, vds_sol = fsolve(solve_exact, [0.6, 1.7])
id_sol = (Vdd - vds_sol) / Rl

print(f"--- THE FINAL NUMBERS ---")
print(f"Set your DC VG to: {vgs_sol:.5f} V")
print(f"Expected VDS:      {vds_sol:.5f} V")
print(f"Expected ID:       {id_sol*1e6:.2f} uA")
