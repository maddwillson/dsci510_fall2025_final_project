import pandas as pd
from pathlib import Path
from src.utils import ensure_parent_dir, save_csv


def load_csv(path):
    df = pd.read_csv(path)

    # parse the Date column
    df["Date"] = pd.to_datetime(df["Date"], utc=True, errors="coerce")

    # Make timezone naive
    df["Date"] = df["Date"].dt.tz_localize(None)

    # Drop rows where date not  parsed
    df = df.dropna(subset=["Date"])

    df = df.sort_values("Date")
    return df


def merge_data():

    # Load individually processed csvs
    yf = load_csv("data/processed/yf_clean.csv")
    google = load_csv("data/processed/google_clean.csv")
    nyt = load_csv("data/processed/nyt_sentiments.csv")
   
    
    # Find the overall date range
    start_date = max(
        yf["Date"].min(),
        google["Date"].min(),
        nyt["Date"].min(),
    )
    end_date = min(
        yf["Date"].max(),
        google["Date"].max(),
        nyt["Date"].max(),
    )

    # Apply date range
    yf = yf[(yf["Date"] >= start_date) & (yf["Date"] <= end_date)]
    google = google[(google["Date"] >= start_date) & (google["Date"] <= end_date)]
    nyt = nyt[(nyt["Date"] >= start_date) & (nyt["Date"] <= end_date)]

    # Merge data
    merged = yf.merge(google, on="Date", how="left")
    merged = merged.merge(nyt, on="Date", how="left")
    
    # Drop days with NaN values
    merged = merged.dropna()

    return merged

if __name__ == "__main__":
    merged = merge_data()
    
    path = "data/final/ibm_df.csv"
    ensure_parent_dir(path)

    # Save to ibm_df    
    save_csv(merged, path)
    print(f"Saved merged dataset to {path}")