import pandas as pd

def load_trends_csv(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=['date'])

    # Ensure 'date' column is datetime type
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def clean_trends_data(df: pd.DataFrame) -> pd.DataFrame:

    # Convert "IBM" column to numeric
    second_col = df.columns[1]
    df[second_col] = pd.to_numeric(df[second_col], errors='coerce')

    # Drop rows with empty values
    df = df.dropna()

    # Rename first column to "Date"
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "Date"})

    # Rename second column to "interest"
    df = df.rename(columns={second_col: "Interest"})

    # Reset index for cleanliness
    df = df.reset_index(drop=True)

    return df

if __name__ == '__main__':
    raw_path = 'data/raw/google_df.csv'
    clean_path = 'data/processed/google_clean.csv'

    df_raw = load_trends_csv(raw_path)
    df_clean = clean_trends_data(df_raw)

    df_clean.to_csv(clean_path, index=False)
    print(f"Cleaned trends data saved to {clean_path}")
