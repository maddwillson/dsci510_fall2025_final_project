import pandas as pd
from pathlib import Path


def load_csv(path):
    # Load csv
    df = pd.read_csv(path)

    # parse the Date column
    df["Date"] = pd.to_datetime(df["Date"])
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

    print(f"Merged date range is from {start_date.date()} to {end_date.date()}")


    # Apply date range
    yf = yf[(yf["Date"] >= start_date) & (yf["Date"] <= end_date)]
    google = google[(google["Date"] >= start_date) & (google["Date"] <= end_date)]
    
    # ---- Reindex NYT to full daily range and forward-fill sentiment ----
    full_index = pd.date_range(start=start_date, end=end_date, freq="D")
    nyt = nyt.set_index("Date").reindex(full_index)
    nyt = nyt.ffill().reset_index().rename(columns={"index": "Date"})

    # Merge data
    merged = yf.merge(google, on="Date", how="inner")
    merged = merged.merge(nyt, on="Date", how="inner")

    # Save to ibm_df
    merged.to_csv("data/final/ibm_df.csv", index=False)
    print(f"Saved merged dataset with {len(merged)} rows → ibm_df.csv")


if __name__ == "__main__":
    merge_data()
    