import pandas as pd
from pathlib import Path
from src.utils import ensure_parent_dir, save_csv

def load_trends_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=['date'])

    # Ensure date is datetime type
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def clean_trends_data(df: pd.DataFrame) -> pd.DataFrame:
    first_col = df.columns[0]
    second_col = df.columns[1]

    # Convert ibm column to numeric
    df[second_col] = pd.to_numeric(df[second_col], errors='coerce')

    # Drop rows with empty values
    df = df.dropna()

    # Rename columns 
    df = df.rename(columns={first_col: "Date", second_col: "Interest"})

    # Ensure Sorted 
    df = df.sort_values("Date")

    # Feature Engineering: Previous Interest 
    df["Interest_lag"] = df["Interest"].shift(1)


    # Reset index for cleanliness
    df = df.reset_index(drop=True)

    return df


if __name__ == '__main__':
    raw_path = 'data/raw/google_df.csv'
    clean_path = 'data/processed/google_clean.csv'

    # Create output directory if needed
    ensure_parent_dir(clean_path)

    df_raw = load_trends_csv(raw_path)
    df_clean = clean_trends_data(df_raw)

    # save
    save_csv(df_clean, clean_path)
    print(f"Cleaned trends data saved to {clean_path}")
