### Google Trends Data
import time
from pytrends.request import TrendReq
from pathlib import Path
from utils import yyyymmdd_to_ymd
from config import (
    START_DATE,
    END_DATE,
)

# format dates for google trends
START = yyyymmdd_to_ymd(START_DATE)
END = yyyymmdd_to_ymd(END_DATE)


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
    return pytrends.interest_over_time()









# RUN GOOGLE LOAD
google_df = load_google_data(kw_list = ["IBM"], tz=360)

# save 
google_df.to_csv("data/raw/google_df.csv", index=True)  # keep index for dates


