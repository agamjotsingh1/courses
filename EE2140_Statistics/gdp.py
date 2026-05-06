import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/gdp.csv")
df = df.dropna(subset=["2024"])

pollutants = df["2024"]

# FREQUENCY HISTOGRAM
plt.figure(figsize=(10, 6))
plt.boxplot(pollutants, orientation="horizontal")
plt.title("Box plot of GDP per capita (in USD$) of different countries")
plt.xlabel("GDP per capita (in USD$)")
plt.savefig("plots/gdp_box_plot.png")
plt.savefig("plots/gdp_box_plot.svg")
plt.show()