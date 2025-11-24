import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def compute_sentiments(nyt_clean_path=f"data/processed/nyt_clean.csv"):
    # Load data
    df = pd.read_csv(nyt_clean_path, parse_dates=["Date"])
    analyzer = SentimentIntensityAnalyzer()

    # Compute sentiment score
    df["Sentiment"] = df["Headline"].apply(
        lambda x: analyzer.polarity_scores(str(x))["compound"] if pd.notna(x) else None
    )
    
    # Average for each day (for when multiple in a day)
    sentiment = df.groupby("Date")[["Sentiment"]].mean().reset_index()

    return sentiment



if __name__ == "__main__":
    df = compute_sentiments()
   
    # Save 
    output_path = f"data/processed/nyt_sentiments.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved sentiment file to: {output_path}")
