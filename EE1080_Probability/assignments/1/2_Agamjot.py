import sys
import pandas as pd
from math import sqrt, log
import matplotlib.pyplot as plt

# Converts a uniform random sample to a bernoulli random sample
def uniform_to_bernoulli(uniform_rv, p):
    if 0 < uniform_rv < p: # bin with size p and 1 - p
        return 1
    else:
        return 0

# Converts a uniform random sample to a exponential random sample
def uniform_to_exp(uniform_rv, lam):
    if uniform_rv == 1: return 0
    return -log(1 - uniform_rv)/lam

def uniform_to_custom_cdfx(uniform_rv):
    '''
    Transforms a uniform random variable into the custom CDFX distribution.

    If 0 <= uniform_x <= 1/3, it returns sqrt(3 * uniform_rv)
    If 2/3 <= uniform_rv <= 1, it returns 6 * uniform_rv - 2
    Otherwise return 2
    '''
    if 0 <= uniform_rv <= 1/3:
        return sqrt(3 * uniform_rv)
    elif 2/3 <= uniform_rv <= 1:
        return 6 * uniform_rv - 2
    else:
        return 2  # Anything in (1/3, 2/3) gets mapped to 2

def process_csv(file_path):
    # Read and display the CSV file
    try:
        df = pd.read_csv(file_path, skiprows=0)
        print(f"Successfully read {file_path}!\n")
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")

if __name__ == "__main__":
    # Print the number of arguments received
    n = len(sys.argv)
    print(f"Total arguments passed: {n}")

    # Print script name
    print(f"\nRunning script: {sys.argv[0]}")

    # Print the arguments
    print("\nArguments received:", sys.argv[1:])
    assert n >= 2, "Not enough arguments provided!"

    # Read the first argument, which determines the mode of operation
    mode_value = int(sys.argv[1])
    print(f"Operating in mode: {mode_value}")

    # Read the second argument, which should be the input file
    input_fn = sys.argv[2]
    uniform_samples = process_csv(input_fn)  # Read uniform samples from CSV
    print(uniform_samples)

    # Get the total number of samples
    N = len(uniform_samples)
    print(f"Total samples (N): {N}")

    assert mode_value == 0 or mode_value == 1 or mode_value == 2, "Invalid mode value"

    # If mode is 0 or 1, we need a third argument (either p or lambda)
    if mode_value == 0:
        assert n >= 3, "Mode 0 requires a probability value (p)!"
        
        # Read the probability value
        p = float(sys.argv[3])

        assert p > 0 and p < 1, "Probability should be between 0 and 1"
        p_str = str(p).strip("0").replace(".", "p")  # Format filename-friendly p value

        # Convert uniform samples to Bernoulli samples (0 or 1 based on p)
        bernoulli_samples = uniform_samples.map(lambda x: uniform_to_bernoulli(x, p))
        bernoulli_samples.rename(columns={'Uniform Samples': 'Bernoulli Samples'}, inplace=True)
        
        # Save results to a new CSV file
        bernoulli_samples.to_csv(f"Bernoulli_{p_str}.csv")
        bernoulli_mean = round(bernoulli_samples.mean()['Bernoulli Samples'], 3)

        # Print the mean of the Bernoulli samples
        print(bernoulli_mean)

    elif mode_value == 1:
        assert n >= 3, "Mode 1 requires a lambda value!"
        
        # Read the lambda value
        lam = float(sys.argv[3])
        assert lam > 0, "Lambda is always greater than 0"

        lam_str = str(lam).strip("0").replace(".", "p")  # Format filename-friendly lambda value

        # Convert uniform samples to exponential samples
        exp_samples = uniform_samples.map(lambda x: uniform_to_exp(x, lam))
        exp_samples.rename(columns={'Uniform Samples': 'Exponential Samples'}, inplace=True)
        
        # Save results to a new CSV file
        exp_samples.to_csv(f"Exponential_{lam_str}.csv")
        print(round(exp_samples.mean()['Exponential Samples'], 3))

        # Plot a histogram of the generated exponential samples
        plt.hist(exp_samples, bins=int(sqrt(N)), label=f"Exponential Samples, Bins = {int(sqrt(N))}")
        plt.legend()
        plt.xlabel("Exponential Samples")
        plt.ylabel("Freqeuncy")
        plt.title(f"Exponential Samples from Uniform Samples with $\\lambda$ = {lam}")
        plt.show()

    else:
        # If mode is anything other than 0 or 1, use the custom CDFX transformation
        cdfx_samples = uniform_samples.map(lambda x: uniform_to_custom_cdfx(x))
        cdfx_samples.rename(columns={'Uniform Samples': 'CDFX Samples'}, inplace=True)
        
        # Save results to a new CSV file
        cdfx_samples.to_csv("CDFX.csv")

        # Count how many times the value 2 appears in the transformed samples
        count_2 = cdfx_samples['CDFX Samples'].value_counts().get(2.0, 0)
        print(count_2)

        # Plot a histogram of the CDFX-transformed samples
        plt.hist(cdfx_samples, bins=int(sqrt(N)), label=f"CDFX Samples, Bins = {int(sqrt(N))}")
        plt.legend()
        plt.xlabel("CDFX Samples")
        plt.ylabel("Freqeuncy")
        plt.title("CDFX Samples from Uniform Samples")
        plt.show()
