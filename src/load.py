### YFINANCE
import yfinance as yf
import pandas as pd


def load_yf_data(ticker="IBM", period="2y"):
    try:
        tick = yf.Ticker(ticker) # set ticker object
        df = tick.history(period) # historical data as pandas df
    except Exception as e:
        raise ConnectionError(f"Failed to fetch data for {ticker}: {e}")
    
    # Check data loaded 
    if df.empty:
        raise ValueError("No data returned from Yahoo Finance.")

    # Add Date column
    df.reset_index(inplace=True)

    return df



### Google Trends Data




### NYT News Data


