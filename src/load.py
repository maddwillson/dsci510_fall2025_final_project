"""
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

"""




### Google Trends Data
"""
Will implement here
"""












### NYT ARTICLE DATA

import requests
from time import sleep


from config import (
    NYT_API_KEY,
    NYT_RATE_LIMIT_SLEEP,
    NYT_DAILY_LIMIT,
    NYT_PAGE_LIMIT,
)

BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"


def get_nyt_page(query, begin_date, end_date, page):
    params = {
        "api-key": NYT_API_KEY,
        "q": query,                                
        "fq": f'headline:("{query}")',             
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


def get_nyt_articles(query, start_date, end_date, max_requests):
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
            page_docs = data["response"]["docs"]
            meta = data["response"]["meta"]
        except Exception as e:
            print(f"Invalid NYT response: {e}")
            break

        # no more pages
        if not page_docs:
            break

        docs.extend(page_docs)

        hits = meta.get("hits", None)
        # safety stop one page before hitting limit
        if (page + 1) * 10 >= (hits or 0):
            break

        sleep(NYT_RATE_LIMIT_SLEEP)

    return docs




