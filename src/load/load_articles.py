### NYT ARTICLE DATA

import requests
from time import sleep
import json
from datetime import datetime
import pandas as pd
from pathlib import Path


from config import (
    NYT_API_KEY,
    NYT_DAILY_LIMIT,
    NYT_RATE_LIMIT_SLEEP,
    NYT_PAGE_LIMIT,
    START_DATE,
    END_DATE,
)



def get_nyt_page(page, query, begin_date, end_date):
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
        raise RuntimeError("NYT rate limit hit")
        
    if response.status_code != 200:
        raise RuntimeError(f"NYT API error {response.status_code}: {response.text}")
   
    return response.json()



def load_nyt_data(query, start_date, end_date, max_requests):
    docs = [] # store articles here
    request_count = 0

    # pull articles from each page
    for page in range(NYT_PAGE_LIMIT):

        if request_count >= max_requests:
            print(f"Reached request limit ({max_requests})")
            break

        print(f"Page {page} (request {request_count+1}/{max_requests})")

        # get one page
        data = get_nyt_page(query, start_date, end_date, page)
        request_count += 1

        # get article info
        try:
            response = data.get("response", {})
            page_docs = response.get("docs") or [] # maybe remove or [] ????
            meta = response.get("meta", {}) # was metadata
        except Exception as e:
            print(f"Invalid NYT response: {e}")
            break

        # no more pages
        if not page_docs:
            break

        docs.extend(page_docs)

        hits = meta.get("hits", 0)
        # safety stop one page before hitting the limit
        if (page + 1) * 10 >= hits:
            break

        sleep(NYT_RATE_LIMIT_SLEEP)

    return docs



#Set Up
BASE_URL = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
QUERY = "IBM"  # can be any keyword

# get articles
articles = load_nyt_data(
    query=QUERY,
    f=START_DATE,
    end_date=END_DATE,
    max_requests= 5 #5 for testing, NYT_DAILY_LIMIT is actually  500
)

# save data
output_path = Path("data/raw/nyt_data.json") 
with open(output_path, "w") as f:
    json.dump(articles, f, indent=2)

# dispaly first five rows
print(pd.json_normalize(articles[:5]).head())
