import json
import pandas as pd
from pathlib import Path

from src.config import QUERY, START_DATE, END_DATE, NYT_DAILY_LIMIT

from src.load.load_articles import load_nyt_data, load_articles_json
from src.load.load_stock import load_yf_data, load_stock_data_csv
from src.load.load_trends import load_google_data, load_trends_csv

from src.process.clean_articles import clean_articles
from src.process.clean_stock import clean_stock_data
from src.process.clean_trends import clean_trends_data
from src.process.merge_data import merge_data
from src.process.sentiment_analysis import compute_sentiments

from analyze.eda import eda
from analyze.modeling import modeling


def load():
    print("Starting data loading...")

    # Load NYT Articles
    articles = load_nyt_data(
        query=QUERY,
        start_date=START_DATE,
        end_date=END_DATE,
        max_requests=NYT_DAILY_LIMIT,
    )
    nyt_raw_path = Path("data/raw/nyt_data.json")
    nyt_raw_path.parent.mkdir(parents=True, exist_ok=True)
    with open(nyt_raw_path, "w") as f:
        json.dump(articles, f, indent=2)
    print(f"Saved NYT raw data to {nyt_raw_path}")

    # Load Yahoo Finance stock data
    yf_df = load_yf_data(START_DATE, END_DATE)
    yf_raw_path = Path("data/raw/yf_df.csv")
    yf_raw_path.parent.mkdir(parents=True, exist_ok=True)
    yf_df.to_csv(yf_raw_path, index=False)
    print(f"Saved YFinance raw data to {yf_raw_path}")

    # Load Google Trends data
    google_df = load_google_data(["IBM"], start_date=START_DATE, end_date=END_DATE, tz=360)
    google_raw_path = Path("data/raw/google_df.csv")
    google_raw_path.parent.mkdir(parents=True, exist_ok=True)
    google_df.to_csv(google_raw_path, index=True)
    print(f"Saved Google Trends raw data to {google_raw_path}")

def clean():
    print("\nStarting data cleaning...")

    # Clean NYT Articles
    nyt_raw_path = Path("data/raw/nyt_data.json")
    nyt_clean_path = Path("data/processed/nyt_clean.csv")
    nyt_clean_path.parent.mkdir(parents=True, exist_ok=True)
    articles = load_articles_json(nyt_raw_path)
    df_nyt_clean = clean_articles(articles)
    df_nyt_clean.to_csv(nyt_clean_path, index=False)
    print(f"Saved cleaned NYT articles to {nyt_clean_path}")

    # Clean Yahoo Finance stock data
    yf_raw_path = Path("data/raw/yf_df.csv")
    yf_clean_path = Path("data/processed/yf_clean.csv")
    yf_clean_path.parent.mkdir(parents=True, exist_ok=True)
    df_yf_raw = load_stock_data_csv(yf_raw_path)
    df_yf_clean = clean_stock_data(df_yf_raw)
    df_yf_clean.to_csv(yf_clean_path, index=False)
    print(f"Saved cleaned Yahoo Finance data to {yf_clean_path}")

    # Clean Google Trends data
    google_raw_path = Path("data/raw/google_df.csv")
    google_clean_path = Path("data/processed/google_clean.csv")
    google_clean_path.parent.mkdir(parents=True, exist_ok=True)
    df_google_raw = load_trends_csv(google_raw_path)
    df_google_clean = clean_trends_data(df_google_raw)
    df_google_clean.to_csv(google_clean_path, index=False)
    print(f"Saved cleaned Google Trends data to {google_clean_path}")


def sentiment_analysis():
    print("\nRunning sentiment analysis...")
    df_sentiments = compute_sentiments()
    sentiment_path = Path("data/processed/nyt_sentiments.csv")
    sentiment_path.parent.mkdir(parents=True, exist_ok=True)
    df_sentiments.to_csv(sentiment_path, index=False)
    print(f"Saved sentiment analysis results to {sentiment_path}")


if __name__ == "__main__":
    #load() (commented out to avoid API overuse)
    clean()
    sentiment_analysis()
    merge_data()
    eda()
    modeling()


        