import pandas as pd

# Load stock data CSV into a DataFrame
def load_stock_data_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=['Date'])

    # Ensure 'Date' is datetime type
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    return df

def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    # Keep only relevant columns
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

    # Drop rows missing critical info
    df = df.dropna(subset=['Date', 'Close'])

    # Ensure price columns are numeric
    price_cols = ['Open', 'High', 'Low', 'Close']
    for col in price_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Remove rows with missing or negative prices
    df = df.dropna(subset=price_cols)
    df = df[(df[price_cols] >= 0).all(axis=1)]

    # clean volume column
    if 'Volume' in df.columns:
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0).astype(int)
        df = df[df['Volume'] >= 0]

    # Remove time and timezone info from Date, keep only YYYY-MM-DD
    df['Date'] = df['Date'].dt.date

    # Reset index for cleanliness
    df = df.reset_index(drop=True)

    return df



if __name__ == '__main__':
    raw_path = 'data/raw/yf_df.csv'
    clean_path = 'data/processed/yf_clean.csv'

    df_raw = load_stock_data_csv(raw_path)
    df_clean = clean_stock_data(df_raw)

    df_clean.to_csv(clean_path, index=False)
    print(f"Cleaned stock data saved to {clean_path}")
