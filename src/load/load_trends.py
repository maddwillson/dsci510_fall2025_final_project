### Google Trends Data
import time
from pytrends.request import TrendReq
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd

from src.config import START_DATE, END_DATE 


# format config dates for google trends API
def format_date(yyyymmdd):
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:]}"


START = format_date(START_DATE)
END = format_date(END_DATE)


# helper for chunking the dates
def daterange(start_date, end_date, step_days):
    current = start_date
    while current < end_date:
        yield current, min(current + timedelta(days=step_days - 1), end_date)
        current += timedelta(days=step_days)


# split the range into <=270-day chunks & stitch together 
def load_google_data(kw_list=["IBM"], start_date=START, end_date=END, tz=360):
    if len(kw_list) != 1:
        raise ValueError("This function currently supports only one keyword")
    keyword = kw_list[0]

    pytrends = TrendReq(hl="en-US", tz=tz)

    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

    max_chunk_days = 270  # Google Trends max daily window

    all_chunks = []

    for chunk_start, chunk_end in daterange(start_date_dt, end_date_dt, max_chunk_days):
        timeframe = f"{chunk_start.strftime('%Y-%m-%d')} {chunk_end.strftime('%Y-%m-%d')}"

        pytrends.build_payload([keyword], timeframe=timeframe, geo="US")
        chunk_df = pytrends.interest_over_time()

        if chunk_df.empty:
            print(f"No data returned for {timeframe}")
            continue

        # Drop 'isPartial' column if exists
        if "isPartial" in chunk_df.columns:
            chunk_df = chunk_df.drop(columns=["isPartial"])

        all_chunks.append(chunk_df)

        time.sleep(3)  

    # Concatenate chunks and remove duplicates
    df = pd.concat(all_chunks)
    df = df[~df.index.duplicated(keep="first")]

    return df


if __name__ == "__main__":
    google_df = load_google_data(["IBM"], start_date=START, end_date=END, tz=360)

    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "google_df.csv"
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    google_df.to_csv(OUTPUT_PATH, index=True)
    print(f"Saved Google Trends DAILY data to: {OUTPUT_PATH}")
