import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datasets/video_game_sales.csv")
df = df.dropna(subset=["Platform"])

# count frequency of each platform type 
platform_frequency = df["Platform"].value_counts()

# exclude platforms below 2% in the pie chart into "others" to avoid cluttering
percentages = platform_frequency / platform_frequency.sum() * 100
main_platforms = platform_frequency[percentages >= 2.0]
others = platform_frequency[percentages < 2.0].sum()

if others > 0:
    main_platforms["Others"] = others

# Plot pie chart
plt.figure(figsize=(6, 6))
plt.pie(
    main_platforms,
    labels=main_platforms.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Pie Chart of Platform for Popular Video games")
plt.axis("equal")
plt.savefig("plots/video_game_sales_pie_chart.png")
plt.savefig("plots/video_game_sales_pie_chart.svg")
plt.show()
