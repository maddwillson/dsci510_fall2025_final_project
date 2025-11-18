
### YFINANCE
import yfinance as yf
import pandas as pd
from datetime import datetime

def load_yf_data(ticker="IBM", period="2y"):
    try:
        tick = yf.Ticker(ticker) # set ticker object
        df = tick.history(period) # historical data as pandas df
    except Exception as e:
        raise ConnectionError(f"Failed to fetch data for {ticker}: {e}")
    
    # Check data loaded 
    if df.empty:
        raise ValueError("No data returned from Yahoo Finance.")

    # Add Date column
    df.reset_index(inplace=True)

    return df










### Google Trends Data
import time
from pytrends.request import TrendReq

def load_google_data(kw_list = ["IBM"], 
                     start_date = '2023-11-14', 
                     end_date = '2025-11-14', 
                     tz=360):
     
    
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






''''''


### NYT ARTICLE DATA

import requests
from time import sleep


from config import (
    NYT_API_KEY,
    NYT_RATE_LIMIT_SLEEP,
    NYT_PAGE_LIMIT,
)

BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"


def get_nyt_page(query, begin_date, end_date, page):
    params = {
        "api-key": NYT_API_KEY,
        "q": query,                                
        "begin_date": begin_date,                  
        "end_date": end_date,
        "page": page                              
    }

    
    response = requests.get(BASE_URL, params=params, timeout=30)

    # Error Handling
    if response.status_code == 429:
        raise RuntimeError("NYT rate limit hit ")
    if response.status_code != 200:
        raise RuntimeError(f"NYT API error {response.status_code}: {response.text}")
    return response.json()


def load_nyt_data(query, start_date, end_date, max_requests):
    docs = [] # store articles here
    request_count = 0

    begin_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    # pull articles from each page
    for page in range(NYT_PAGE_LIMIT):

        if request_count >= max_requests:
            print(f"Reached request limit ({max_requests})")
            break

        print(f"Page {page} (request {request_count+1}/{max_requests})")

        # get one page
        data = get_nyt_page(query, begin_str, end_str, page)
        request_count += 1

        # get article info
        try:
            response = data.get("response", {})
            page_docs = response.get("docs") or []
            meta = response.get("metadata", {})
        except Exception as e:
            print(f"Invalid NYT response: {e}")
            break

        # no more pages
        if not page_docs:
            break

        docs.extend(page_docs)

        hits = meta.get("hits", 0)
        # safety stop one page before hitting limit
        if (page + 1) * 10 >= hits:
            break

        sleep(NYT_RATE_LIMIT_SLEEP)

    return docs
