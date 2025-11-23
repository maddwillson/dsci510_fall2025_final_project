import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pathlib import Path

text_cols = ["Headline", "Abstract", "Snippet"]

def compute_sentiments(nyt_clean_path=f"data/processed/nyt_clean.csv"):
    df = pd.read_csv(nyt_clean_path, parse_dates=["Date"])
    analyzer = SentimentIntensityAnalyzer()


    # Sentiment extraction helper
    def get_sentiment_dict(text):

        # handle NaN/None values
        if not isinstance(text, str):
            text = ""
        s = analyzer.polarity_scores(text)
        return {
            "pos": s["pos"],
            "neg": s["neg"],
            "neu": s["neu"],
            "compound": s["compound"],
        }

    # Sentiment Analysis for each text field 
    for col in text_cols:
        sentiment_output = df[col].apply(get_sentiment_dict).apply(pd.Series)
        sentiment_output = sentiment_output.add_prefix(f"{col}_")
        df = pd.concat([df, sentiment_output], axis=1)

    # Aggregate articles by day
    agg_dict = {}

    # Make Columns
    for col in text_cols:
        prefix = col + "_"
        agg_dict[prefix + "pos"] = "mean"
        agg_dict[prefix + "neg"] = "mean"
        agg_dict[prefix + "neu"] = "mean"
        agg_dict[prefix + "compound"] = ["mean", "median"]

    # Add article count column
    df["Count"] = 1 # initalize
    daily = df.groupby("Date").agg(agg_dict)
    daily.columns = ["_".join(col).strip() for col in daily.columns] 
    daily["Article_Count"] = df.groupby("Date")["Count"].sum() # get counts

    # Sort by date
    daily = daily.reset_index().sort_values("Date")


    return daily


if __name__ == "__main__":
    df = compute_sentiments()
   
    # Save 
    output_path = f"data/processed/nyt_sentiments.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved sentiment file to: {output_path}")
