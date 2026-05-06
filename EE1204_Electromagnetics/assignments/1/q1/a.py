


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch

# Constants
d = 1  # Distance between charges in meters

def plot_charge_distribution(case="equal"):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Set up the axes
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_xlabel('x (m)', fontsize=12)
    ax.set_ylabel('z (m)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    ax.set_aspect('equal')
    
    # Position of charges
    z1 = d/2
    z2 = -d/2
    
    # Add position vectors to several points
    position_points = [(0.5, 0.5), (1.0, 0), (0, 1.0), (-0.8, 0.4), (0, -0.7)]
    for x, z in position_points:
        # Draw position vector
        arrow = FancyArrowPatch((0, 0), (x, z), 
                               arrowstyle='->', 
                               mutation_scale=15, 
                               color='green', 
                               linewidth=1.5)
        ax.add_patch(arrow)
        ax.text(x+0.05, z+0.05, r'$\vec{r}$', color='green', fontsize=12)
    
    # Plot the charges
    if case == "equal":
        # Two positive charges
        positive_charge1 = Circle((0, z1), 0.1, color='red', alpha=0.7)
        positive_charge2 = Circle((0, z2), 0.1, color='red', alpha=0.7)
        ax.add_patch(positive_charge1)
        ax.add_patch(positive_charge2)
        ax.text(0.15, z1, '+q', fontsize=14)
        ax.text(0.15, z2, '+q', fontsize=14)
        ax.set_title('Charge Distribution: Two Equal Positive Charges at z = ±d/2', fontsize=14)
    
    elif case == "opposite":
        # One positive, one negative charge
        positive_charge = Circle((0, z1), 0.1, color='red', alpha=0.7)
        negative_charge = Circle((0, z2), 0.1, color='blue', alpha=0.7)
        ax.add_patch(positive_charge)
        ax.add_patch(negative_charge)
        ax.text(0.15, z1, '+q', fontsize=14)
        ax.text(0.15, z2, '-q', fontsize=14)
        ax.set_title('Charge Distribution: Opposite Charges at z = ±d/2', fontsize=14)
    
    # Add x and z axes labels
    ax.text(1.9, 0.1, 'x', fontsize=12)
    ax.text(0.1, 1.9, 'z', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(f'charge_distribution_{case}_with_r.png', dpi=300)
    plt.show()

# Plot both charge distributions
plot_charge_distribution(case="equal")
plot_charge_distribution(case="opposite")

