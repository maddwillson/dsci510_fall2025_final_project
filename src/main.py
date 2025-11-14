from load import load_yf_data, get_nyt_articles
import pandas as pd
import yfinance as yf
import json
from datetime import datetime
from config import NYT_DAILY_LIMIT


if __name__ == "__main__":
    """
    # YFINANCE
    yf_df = load_yf_data()

    #download if needed
    #yf_df.to_csv("yf_df.csv", index=False)
    """

    # GOOGLE
    """
    to be implemented 
    """   





    # NYT
    query = "IBM"  # choose any keyword
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 5)

    # get articles
    articles = get_nyt_articles(
        query=query,
        start_date=start,
        end_date=end,
        max_requests=NYT_DAILY_LIMIT
    )

    # save data
    output_file = "nyt_raw_articles.json"
    with open(output_file, "w") as f:
        json.dump(articles, f, indent=2)


        