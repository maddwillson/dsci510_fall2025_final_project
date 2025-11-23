
### YFINANCE
import yfinance as yf
import pandas as pd
from datetime import datetime
from pathlib import Path


from config import START_DATE, END_DATE

def load_yf_data(ticker="IBM"):
    try:
        tick = yf.Ticker(ticker) # set ticker object
        df = tick.history(start=START_DATE, end=END_DATE) # historical data as pandas df
    except Exception as e:
        raise ConnectionError(f"Failed to fetch data for {ticker}: {e}")
    
    # Check data loaded 
    if df.empty:
        raise ValueError("No data returned from Yahoo Finance.")

    # Add Date column
    df.reset_index(inplace=True)

    # Sort chronologically
    df = df.sort_values("Date")
    
    return df





if __name__ == "__main__":
    ##### RUN YFINANCE
    yf_df = load_yf_data()

    output_path = "./data/raw/yf_df.csv"

    # Save raw file
    yf_df.to_csv(output_path, index=False)
    print(f"Saved YFINANCE Stock data to: {output_path}")

    print(yf_df.head(1))
    print("\n")
    print(yf_df.tail(1))
