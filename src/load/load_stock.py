
### YFINANCE
import yfinance as yf
import pandas as pd
from datetime import datetime

from src.config import START_DATE, END_DATE

def load_yf_data(start_date, end_date, ticker = "IBM"):
    try:
        # Convert config dates to YYYY-MM-DD strings for yfinance
        start_date = datetime.strptime(start_date, "%Y%m%d").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y%m%d").strftime("%Y-%m-%d")

        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            actions=False,     
            auto_adjust=False  
        )
    except Exception as e:
        raise ConnectionError(f"Failed to fetch data: {e}")

    # Check data loaded 
    if df.empty:
        raise ValueError("No data returned from Yahoo Finance.")

    # Add Date column
    df.reset_index(inplace=True)

    # Flatten multiindex columns 
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [' '.join(col).strip() for col in df.columns.values]

    # fix naming
    df.columns = [col.replace(' IBM', '') for col in df.columns]

    # Ensure date column is datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='raise')

    # Sort 
    df = df.sort_values("Date")
    
    return df





if __name__ == "__main__":
    ##### RUN YFINANCE
    yf_df = load_yf_data(START_DATE, END_DATE)

    output_path = "./data/raw/yf_df.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)


    # Save raw file
    yf_df.to_csv(output_path, index=False)
    print(f"Saved YFINANCE Stock data to: {output_path}")

