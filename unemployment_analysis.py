import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv("data/unemployment.csv")

# Clean column names
data.columns = [col.strip().replace(' ', '_').lower() for col in data.columns]

# Convert date column to datetime
data['date'] = pd.to_datetime(data['date'], errors='coerce')

# Drop rows with missing values
data.dropna(subset=['date', 'estimated_unemployment_rate_(%)'], inplace=True)

# National monthly average
monthly_avg = data.groupby(data['date'].dt.to_period('M'))['estimated_unemployment_rate_(%)'].mean()
monthly_avg.index = monthly_avg.index.to_timestamp()

plt.figure(figsize=(10, 5))
plt.plot(monthly_avg.index, monthly_avg.values, marker='o', linestyle='-')
plt.title("Monthly Average Unemployment Rate")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate (%)")
plt.grid(True)
plt.tight_layout()
plt.show()

# Heatmap by region
pivot = data.pivot_table(index='region', columns='date', values='estimated_unemployment_rate_(%)')
plt.figure(figsize=(12, 6))
sns.heatmap(pivot, cmap="coolwarm", linecolor='white', linewidths=0.1)
plt.title("Unemployment Heatmap by Region")
plt.tight_layout()
plt.show()

# Covid-19 impact analysis
pre_covid = data[data['date'] < '2020-03-01']
post_covid = data[data['date'] >= '2020-03-01']

print("\nAverage Unemployment Rate Before COVID-19:", pre_covid['estimated_unemployment_rate_(%)'].mean())
print("Average Unemployment Rate During/Post COVID-19:", post_covid['estimated_unemployment_rate_(%)'].mean())
