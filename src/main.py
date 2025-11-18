from load import load_google_data#, load_nyt_data, load_yf_data
import pandas as pd
import yfinance as yf
import json
from datetime import datetime
from config import NYT_DAILY_LIMIT
from pytrends.request import TrendReq



if __name__ == "__main__":
    # YFINANCE
    #yf_df = load_yf_data()

    #download if needed
    #yf_df.to_csv("yf_df.csv", index=False)









    # GOOGLE
    google_df = load_google_data(kw_list = ["IBM"], tz=360)

    #download if needed
    google_df.to_csv("google_df.csv", index=False)





    '''

    # NYT
    query = "IBM"  # choose any keyword

    # define range (2 years gave 227 articles)
    start = datetime(2023, 11, 14)
    end = datetime(2025, 11, 13)

    # get articles
    articles = load_nyt_data(
        query=query,
        start_date=start,
        end_date=end,
        max_requests= 50 #NYT_DAILY_LIMIT
    )

    # save data
    output_file = "nyt_raw_articles.json" 
    with open(output_file, "w") as f:
        json.dump(articles, f, indent=2)
    '''

        