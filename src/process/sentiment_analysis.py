import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Columns that need sentiment scores
text_cols = ["Headline", "Abstract", "Snippet"]

def compute_sentiments(nyt_clean_path=f"data/processed/nyt_clean.csv"):
    # Load data
    df = pd.read_csv(nyt_clean_path, parse_dates=["Date"])
    analyzer = SentimentIntensityAnalyzer()

    # Helper for sentiment score
    def get_compound(text):
        if pd.isna(text):
            return None
        return analyzer.polarity_scores(str(text))["compound"]

    # Sentiment Analysis for each column 
    for col in text_cols:
        df[col + "_Sentiment"] = df[col].apply(get_compound)
    
    
    sentiment = df.groupby("Date")[[col + "_Sentiment" for col in text_cols]].mean().reset_index()


    return sentiment



if __name__ == "__main__":
    df = compute_sentiments()
   
    # Save 
    output_path = f"data/processed/nyt_sentiments.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved sentiment file to: {output_path}")
