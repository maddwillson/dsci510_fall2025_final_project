### Google Trends Data
import time
from pytrends.request import TrendReq
from pathlib import Path
from src.config import START_DATE, END_DATE



# format dates for google trends
def format_date(yyyymmdd):
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:]}"


START = format_date(START_DATE)
END = format_date(END_DATE)

def load_google_data(kw_list = ["IBM"], 
                     start_date = START, 
                     end_date = END, 
                     tz=360
                     ):
    if len(kw_list) > 5:
        raise ValueError("kw_list must be 5 or less key words") 
    
    # Add a realistic browser header so Google does not block you
    headers = {
        "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
    }
    
    pytrends = TrendReq(hl='en-US', 
                    tz=tz, # tz: timezone offset (360 is US CST) 
                    timeout=(10,25), 
                    retries=3, 
                    backoff_factor=0.4,
                    requests_args={"headers": headers}
                    ) 
    time.sleep(8) 

    # Build request payload
    pytrends.build_payload(kw_list, 
                           cat=0, 
                           timeframe=f'{start_date} {end_date}', 
                           geo='US', 
                           gprop='')
    
    time.sleep(8) 

    # return df of historical data for when the keyword was searched most
    df = pytrends.interest_over_time()
    if df.empty:
        raise ValueError("Google Trends returned an empty DataFrame")
    return df









# RUN GOOGLE LOAD
if __name__ == "__main__":
    google_df = load_google_data(["IBM"], tz=360)

    # Always save to project/data/raw/google_df.csv
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "google_df.csv"

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    google_df.to_csv("data/raw/google_df.csv", index=True)  # keep index for dates
    print(f"Saved Google Trends data to: {OUTPUT_PATH}")

