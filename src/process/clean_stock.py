import pandas as pd

def load_stock_data_csv(filepath: str) -> pd.DataFrame:
    
    # remove IBM suffix
    df_raw = pd.read_csv(filepath)
    df_raw.columns = [col.replace(' IBM', '') for col in df_raw.columns]

    # load with date parsing
    df = pd.read_csv(filepath, parse_dates=['Date'], dayfirst=False)
    
    # remove IBM suffix in parsed df too
    df.columns = [col.replace(' IBM', '') for col in df.columns]

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    df = df.dropna(subset=['Date'])

    # Normalize date
    df['Date'] = df['Date'].dt.normalize()

    df = df.sort_values('Date')
    return df


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    # Keep only relevant columns
    df = df[['Date', 'Close', 'Volume']].copy()  # avoid SettingWithCopyWarning

    # Ensure numeric types
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')

    # Drop rows with no close
    df = df.dropna(subset=['Close'])

    # Remove negative prices
    df = df[df['Close'] >= 0]

    df = df.sort_values('Date')

    # Compute daily return
    df['Return'] = df['Close'].pct_change()


    # Feature engineering: Return Lag, average returns, Rolling Volatility, Day of Week
    df['Return_lag'] = df['Return'].shift(1) # previous day
    df['Return_3d'] = df['Return'].rolling(window=3).mean().shift(1) # 3 day avg
    df['Return_7d'] = df['Return'].rolling(window=7).mean().shift(1) # 7 day avg
    df['Volatility_3d'] = df['Return'].rolling(window=3).std() # 3 day voltility
    df['Volatility_7d'] = df['Return'].rolling(window=7).std() # 7 day voltility
    df['DayOfWeek'] = df['Date'].dt.day_name()

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
