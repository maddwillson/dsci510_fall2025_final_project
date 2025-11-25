import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Plot settings
sns.set(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (12, 6)

# Paths
data_path = Path(__file__).parent.parent.parent / "data/final/ibm_df.csv"
results_path = Path(__file__).parent.parent.parent / "results"
results_path.mkdir(parents=True, exist_ok=True)

variables = [
    'Close', 'Volume', 'Return', 'Return_lag', 'Return_3d_sum', 'Return_7d_sum',
    'Volatility_3d', 'Volatility_7d', 'Interest', 'Interest_lag',
    'Sentiment', 'Prev_sentiment'
]

def scale_series(series, new_min=-0.05, new_max=0.05):
    s_min = series.min()
    s_max = series.max()
    return (series - s_min) / (s_max - s_min) * (new_max - new_min) + new_min


def eda():
    df = pd.read_csv(data_path, parse_dates=["Date"])

    print("\nData Preview:\n", df.head(2))
    rows, cols = df.shape
    print(f"Dataset Shape: Rows={rows:,}, Columns={cols}")
    print("Columns:", df.columns.tolist())
    print("\nMissing values:\n", df.isna().sum())
    print("\nSummary Stats:\n", df.describe())

    figures = {}

    # Distributions of variables 
    fig, ax = plt.subplots(4, 3, figsize=(20, 15))
    ax = ax.flatten()
    for i, var in enumerate(variables):
        sns.histplot(df[var], kde=True, bins=30, ax=ax[i])
        ax[i].set_title(f'Distribution of {var}')
    plt.tight_layout()
    figures["variable_distributions"] = fig

    # Correlation heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(df[variables].corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
    ax.set_title("Correlation Heatmap")
    figures["corr_heatmap"] = fig

    # Explore Interest and Sentiment Shapes
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    sns.scatterplot(x='Interest', y='Return', data=df, ax=axes[0])
    axes[0].set_title('Stock Return vs Google Interest')

    sns.scatterplot(x='Sentiment', y='Return', data=df, ax=axes[1])
    axes[1].set_title('Stock Return vs NYT Sentiment')
    plt.tight_layout()
    figures["interest_sentiment_scatter"] = fig

    # Day of the Week Analysis
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        x='DayOfWeek',
        y='Return',
        data=df,
        order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
        ax=ax
    )
    ax.set_title("Return Distribution by Day of Week")
    figures["return_by_dayofweek"] = fig

    # Pairplot for relationships
    fig = sns.pairplot(df[['Return', 'Return_lag', 'Return_3d_sum', 'Return_7d_sum',
                           'Volatility_7d', 'Interest', 'Interest_lag',
                           'Sentiment', 'Prev_sentiment']])
    figures["pairplot"] = fig.fig  # pairplot stores fig at `.fig`

    # Scale series for time series plotting
    df['Return_scaled'] = scale_series(df['Return'])
    df['Interest_scaled'] = scale_series(df['Interest'])
    df['Sentiment_scaled'] = scale_series(df['Sentiment'])
    
    # Time Series Plot
    fig, ax = plt.subplots(figsize=(14, 6))
    for col in ['Return_7d_sum', 'Volatility_7d', 'Interest_scaled', 'Sentiment_scaled']:
        ax.plot(df['Date'], df[col], label=col)
    ax.set_title("Scaled Time Series of Returns, Volatility, Interest & Sentiment")
    ax.set_xlabel("Date")
    ax.set_ylabel("Scaled Value")
    ax.legend()
    plt.tight_layout()
    figures["time_series"] = fig

    return figures


if __name__ == "__main__":
    figs = eda()

    # Save figures
    for name, fig in figs.items():
        save_path = results_path / f"{name}.png"
        fig.savefig(save_path)
        plt.close(fig)

    print("Figures saved to:", results_path)
