import random

# Set the seed for reproducibility
random.seed(42)

# Define the maximum number of trials
# To avoid overflow, we set a limit for maximum number of trails
max_trials = int(1e10)

# Simulates a Bernoulli trial
# p -> Probability of success
def bernoulli(p):
    n = random.uniform(0, 1)  # Generate a uniform random variable sample in [0, 1]
    assert p > 0, 'Probability should be greater than 0'

    # Binning [0, 1] into two parts -> [0, p] and (p, 1]
    # Probability of [0, p] -> p
    # Probability of (p, 1] -> 1 - p
    if n < p:
        return 1  # Heads 
    else:
        return 0  # Tails

def sim_petersburg(m):
    '''
    Simulates St. Petersburg paradox.

    m -> The number of times the game is played.
    Returns the average reward over m simulations.
    '''
    total_reward = 0
    p = 0.5 # Fair coin is assumed

    for _ in range(m):  # Repeat the game m times
        
        # Coin is tossed until tails appear
        # or when number of tosses exceeds max_trials
        for i in range(max_trials):
            is_heads = bernoulli(p)

            if not is_heads:  # Stop when tails appears
                total_reward += 2**(i + 1)
                break

    return (total_reward / m) 

# Run the simulation with different numbers of games, and round till 3 decimal places
print(round(sim_petersburg(100), 3), round(sim_petersburg(10000), 3), round(sim_petersburg(1000000), 3))
