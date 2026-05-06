import random
import matplotlib.pyplot as plt
import numpy as np
import sys

random.seed(42) # Set seed for reproducibility

# Get the mode and N value from CLI arguments
mode, N = int(sys.argv[1]), int(sys.argv[2])
assert N > 0, "N should be greater than 0"
assert mode == 0 or mode == 1 or mode == 2, "Invalid mode provided"

if mode == 0:
    '''
    Mode 0

    Angle made by chord w.r.t a tangent at one fixed end is equally likely.

    Theta is a uniform RV from 0 to pi.
    Chord is selected such that it makes angle theta with tangent at (0, 1).
    '''

    # Generate X from a uniform theta sample
    # X -> Chord Length for a particular theta
    def gen_X(theta):
        return 2*np.sin(theta)

    # Generate uniform theta from 0 to pi
    def gen_uniform_theta():
        return random.uniform(0, np.pi)

    fav = 0 # Favourable number of outputs
    theta_samples = [ gen_uniform_theta() for _ in range(N)] # Generate N uniform theta samples 
    X_samples = []

    for theta in theta_samples:
        X = gen_X(theta)
        X_samples.append(X)

        if(X >= np.sqrt(3)): # Chord length is greater than root(3)
            fav += 1

    print("Fraction of chord length >= sqrt(3) -> ", fav/N)
    plt.hist(X_samples, bins=int(np.sqrt(N))) # Plot the histgram with bins as sqrt(N) rule
    plt.xlabel("Chord Length")
    plt.ylabel("Frequency")
    plt.title("Mode 0")
    plt.show()

elif mode == 1:
    '''
    Mode 1

    Distance of the chord from center is equally likely.

    U -> distance of chord from center.
    U is a uniform RV from 0 to 1.
    '''

    # Generate X from a uniform U sample
    # X -> Chord Length for a particular U
    def gen_X(U):
        return 2*np.sqrt(1 - U*U)

    # Generate uniform U from 0 to 1
    def gen_uniform_U():
        return random.uniform(0, 1)

    fav = 0 # Favourable number of outputs 
    U_samples = [gen_uniform_U() for _ in range(N)] # Generate N uniform U samples 
    X_samples = []

    for U in U_samples:
        X = gen_X(U)
        X_samples.append(X)

        if(X >= np.sqrt(3)): # Chord length is greater than root(3)
            fav += 1

    print("Fraction of chord length >= sqrt(3) -> ", fav/N)
    plt.hist(X_samples, bins=int(np.sqrt(N)))  # Plot the histgram with bins as sqrt(N) rule
    plt.xlabel("Chord Length")
    plt.ylabel("Frequency")
    plt.title("Mode 1")
    plt.show()

elif mode == 2:
    '''
    Mode 2

    Center of the chord is equally likely within circle.

    U -> uniform RV from 0 to 1.
    R -> distance of a randomly selected point (X, Y) on the circle from the center
    Z -> length of chord length as a function of R
    '''

    # Generate R sample from uniform U sample
    def gen_R(U):
        return np.sqrt(U)

    # Generate Z sample from R sample
    def gen_Z(R):
        return 2*np.sqrt(1 - R*R)

    # Generate uniform U sample between 0 to 1
    def gen_uniform_U():
        return random.uniform(0, 1)

    fav = 0 # Number of favourable outputs
    U_samples = [gen_uniform_U() for _ in range(N)] # Generate N uniform U samples 

    Z_samples = []
    for U in U_samples:
        R = gen_R(U)
        Z = gen_Z(R)

        Z_samples.append(Z)
        if (Z >= np.sqrt(3)): # Chord length is greater than root(3)
            fav += 1

    print("Fraction of chord length >= sqrt(3) -> ", fav/N)
    plt.hist(Z_samples, bins=int(np.sqrt(N)))
    plt.xlabel("Chord Length")
    plt.ylabel("Frequency")
    plt.title("Mode 2")
    plt.show()
