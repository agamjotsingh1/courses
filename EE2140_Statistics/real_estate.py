import pandas as pd
import matplotlib.pyplot as plt

BINS = 50

df = pd.read_csv("datasets/real_estate.csv")
df = df.dropna(subset=["price_in_USD"])

prices = df["price_in_USD"]

# exclude prices more than 1.5 million
# these are extreme outliers
prices = prices[prices <= 1.5e6]

# FREQUENCY HISTOGRAM
plt.figure(figsize=(16, 6))
prices.hist(bins=BINS, edgecolor='black')
plt.title("Frequency Histogram for Price (in USD) of Real Estate in the World")
plt.xlabel("Price (in USD)")
plt.ylabel("Real Estate Frequency")
plt.savefig("plots/real_estate_frequency_histogram.png")
plt.savefig("plots/real_estate_frequency_histogram.svg")
plt.show()

# RELATIVE FREQUENCY HISTOGRAM
plt.figure(figsize=(16, 6))
prices.hist(bins=BINS,
            edgecolor='black',
            weights=[1/len(prices)]*len(prices),
            color="orange")
plt.title("Relative frequency Histogram for Price (in USD) of Real Estate in the World")
plt.xlabel("Price (in USD)")
plt.ylabel("Real estate relative frequency")
plt.savefig("plots/real_estate_relative_frequency_histogram.png")
plt.savefig("plots/real_estate_relative_frequency_histogram.svg")
plt.show()
