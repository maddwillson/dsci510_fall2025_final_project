
### YFINANCE
import yfinance as yf
import pandas as pd
from datetime import datetime

from config import QUERY

def load_yf_data(ticker=QUERY, period="5y"):
    try:
        tick = yf.Ticker(ticker) # set ticker object
        df = tick.history(period=period) # historical data as pandas df
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






##### RUN YFINANCE
yf_df = load_yf_data()

# Save raw file
yf_df.to_csv("./data/raw/yf_df.csv", index=False)
print(yf_df.head(1))
print("\n")
print(yf_df.tail(1))
