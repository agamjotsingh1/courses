import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("./datasets/landslide.csv")
df['event_date'] = pd.to_datetime(df['event_date'], errors='coerce')
df = df.dropna(subset=['event_date'])

# data before 2025 is extremely sparse and unreliable
# remove years before 2025
df = df[df['event_date'].dt.year >= 2005]

# %b = Jan, Feb, Mar ...
df['month_year'] = df['event_date'].dt.strftime('%b %Y')  
frequency = df['month_year'].value_counts()

# sort chronologically
frequency.index = pd.to_datetime(frequency.index, format='%b %Y')
frequency = frequency.sort_index()

# convert back to string for plotting
frequency.index = frequency.index.strftime('%b %Y')

# FREQUENCY TABLE
frequency.to_csv('tables/landslide_frequency_table.csv') 

# FREQUENCY POLYGON

plt.figure(figsize=(16, 6))
plt.plot(frequency.index, frequency.values, marker="o")

plt.xlabel("Year")
plt.ylabel("Number of Landslides")
plt.title("Frequency Polygon of Landslides (2005 onwards)")

# show label every 6 months
step = 2
plt.xticks(
    range(0, len(frequency.index), step),
    frequency.index[::step],
    rotation=90,
    fontsize=8
)

plt.tight_layout()
plt.savefig("plots/landslide_frequency_polygon.png")
plt.savefig("plots/landslide_frequency_polygon.svg")
plt.show()

# BAR DIAGRAM

plt.figure(figsize=(16, 6))
plt.bar(frequency.index, frequency.values)

plt.xlabel("Month")
plt.ylabel("Number of Landslides")
plt.title("Bar diagram of Landslides (2005 onwards)")

# show label every 6 months
step = 2
plt.xticks(
    range(0, len(frequency.index), step),
    frequency.index[::step],
    rotation=90,
    fontsize=8
)

plt.tight_layout()
plt.savefig("plots/landslide_bar_diagram.png")
plt.savefig("plots/landslide_bar_diagram.svg")
plt.show()

# BAR DIAGRAM (Vertical)

plt.figure(figsize=(6, 16))
plt.barh(frequency.index, frequency.values)

plt.ylabel("Month")
plt.xlabel("Number of Landslides")
plt.title("Bar diagram of Landslides (2005 onwards)")

# show label every 6 months
step = 2
plt.yticks(
    range(0, len(frequency.index), step),
    frequency.index[::step],
    fontsize=8
)

plt.tight_layout()
plt.savefig("plots/landslide_bar_diagram_vertical.png")
plt.savefig("plots/landslide_bar_diagram_vertical.svg")
plt.show()