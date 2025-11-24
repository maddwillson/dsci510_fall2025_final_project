import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pathlib import Path

def compute_sentiments(nyt_clean_path="data/processed/nyt_clean.csv"):
    # Load data
    df = pd.read_csv(nyt_clean_path, parse_dates=["Date"])
    analyzer = SentimentIntensityAnalyzer()

    # Compute sentiment score
    df["Sentiment"] = df["Headline"].apply(
        lambda x: analyzer.polarity_scores(str(x))["compound"] if pd.notna(x) else None
    )
    
    # Average for each day (for when multiple in a day)
    sentiment = df.groupby("Date")[["Sentiment"]].mean().reset_index()

    # Feature Engineering
    sentiment = sentiment.sort_values("Date")
    sentiment["Prev_sentiment"] = sentiment["Sentiment"].shift(1)     # prev sentiment
    sentiment["Days_since_prev"] = sentiment["Date"].diff().dt.days   # find days since prev article
    sentiment.loc[sentiment["Days_since_prev"] > 14, "Prev_sentiment"] = 0.0  # drop old sentiments
    sentiment = sentiment.drop(columns=["Days_since_prev"])  # remove helper col

    return sentiment



if __name__ == "__main__":
    df = compute_sentiments()
   
    # Save 
    output_path = "data/processed/nyt_sentiments.csv"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Saved sentiment file to: {output_path}")
