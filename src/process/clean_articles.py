import json
import pandas as pd


def load_articles_json(filepath: str) -> list:
    #Load raw JSON file (list of dicts)
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected JSON to be a list of article objects.")

    return data


def clean_articles(data: list) -> pd.DataFrame:

    # Convert to DataFrame
    df = pd.DataFrame(data)


    # Extract headline_main
    df['headline_main'] = df['headline'].apply(
        lambda x: x.get('main') if isinstance(x, dict) else None
    )

    # Keep only useful columns
    df = df[['pub_date', 'headline_main']]

    
    # Remove articles missing any value
    df = df.dropna()


    # Clean pub_date
    df['pub_date'] = pd.to_datetime(df['pub_date'], errors='coerce')
    df = df.dropna(subset=['pub_date'])
    df['pub_date'] = df['pub_date'].dt.date


    # Rename columns
    df = df.rename(columns={"pub_date": "Date", 
                            "headline_main": "Headline"})

    df = df.reset_index(drop=True)
    return df


if __name__ == '__main__':
    raw_path = 'data/raw/nyt_data.json'
    clean_path = 'data/processed/nyt_clean.csv'

    articles = load_articles_json(raw_path)
    df_clean = clean_articles(articles)

    df_clean.to_csv(clean_path, index=False)
    print(f"Cleaned NYT article data saved to {clean_path}")
