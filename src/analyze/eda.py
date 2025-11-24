import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from pathlib import Path

# Plot settings
sns.set(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12,6)

# Get path
data_path = Path(__file__).parent.parent.parent / "data/final/ibm_df.csv"  # relative to src/ folder
results_path = Path(__file__).parent.parent.parent / "results"

# Load data
df = pd.read_csv(data_path, parse_dates=["Date"])
print("\nData Preview:\n", df.head(2))

# Shape
rows, cols = df.shape
print(f"Dataset Shape: Rows={rows:,}, Columns={cols}")


# Columns
print(df.columns.tolist())

# Missing Values (should all be 0)
print("\nMissing values:\n", df.isna().sum())

# Summary Stats
print("\nSummary Stats:\n",df.describe())



# Distributions of variables 
variables = ['Close', 'Volume', 'Return', 'Return_lag', 'Return_3d', 'Return_7d',
             'Volatility_3d', 'Volatility_7d', 'Interest', 'Interest_lag', 'Sentiment', 'Prev_sentiment']
plt.figure(figsize=(20,15))
for i, var in enumerate(variables, 1):
    plt.subplot(4,3,i)
    sns.histplot(df[var], kde=True, bins=30)
    plt.title(f'Distribution of {var}')
plt.tight_layout()
#plt.show()
plt.savefig(results_path / "variable_distributions.png")
plt.close()


# Correlation heatmap
numeric_vars = ['Return', 'Return_lag', 'Return_3d', 'Return_7d',
                'Volatility_3d', 'Volatility_7d', 'Interest', 'Interest_lag', 
                'Sentiment', 'Prev_sentiment']
plt.figure(figsize=(10,8))
sns.heatmap(df[numeric_vars].corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title("Correlation Heatmap")
#plt.show()
plt.savefig(results_path / "corr_heatmap.png")
plt.close()



# Explore Interest and Sentiment Shapes
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)  # Return vs Google Interest
sns.scatterplot(x='Interest', y='Return', data=df)
plt.title('Stock Return vs Google Interest')
plt.subplot(1,2,2)  # Return vs NYT Sentiment
sns.scatterplot(x='Sentiment', y='Return', data=df)
plt.title('Stock Return vs NYT Sentiment')
plt.tight_layout()
#plt.show()
plt.savefig(results_path / "interest_sentiment_scatter.png")
plt.close()


# Day of the Week Analysis
plt.figure(figsize=(10,6))
sns.boxplot(x='DayOfWeek', y='Return', data=df,
            order=['Monday','Tuesday','Wednesday','Thursday','Friday'])
plt.title("Return Distribution by Day of Week")
#plt.show()
plt.savefig(results_path / "return_by_dayofweek.png")
plt.close()



# Pairplot for relationships
sns.pairplot(df[['Return', 'Return_lag', 'Return_3d', 'Return_7d', 'Volatility_7d', 
                 'Interest', 'Interest_lag', 'Sentiment', 'Prev_sentiment']])
#plt.show()
plt.savefig(results_path / "pairplot.png")
plt.close()





# Scale series for time series plotting
def scale_series(series, new_min=-0.05, new_max=0.05):
    s_min = series.min()
    s_max = series.max()
    return (series - s_min) / (s_max - s_min) * (new_max - new_min) + new_min

df['Return_scaled'] = scale_series(df['Return'])
df['Interest_scaled'] = scale_series(df['Interest'])
df['Sentiment_scaled'] = scale_series(df['Sentiment'])

# Time Series Plot
df_to_plot = ['Return_scaled', 'Return_3d', 'Return_7d', 'Volatility_7d', 'Interest_scaled', 'Sentiment_scaled']
plt.figure(figsize=(14,6))
for col in df_to_plot:
    plt.plot(df['Date'], df.get(col, df[col]), label=col)
plt.title("Scaled Time Series of Returns, Volatility, Interest & Sentiment")
plt.xlabel("Date")
plt.ylabel("Scaled Value")
plt.legend()
plt.tight_layout()
#plt.show()
plt.savefig(results_path / "time_series.png")
plt.close()

