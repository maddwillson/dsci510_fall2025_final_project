# NYT CONFIG
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

# get api key from .env
load_dotenv()
NYT_API_KEY = os.getenv("NYT_API_KEY")

# 2 years
START_DATE = datetime(2023, 11, 14)
END_DATE = datetime(2023, 11, 13)

# NYT API constraints
NYT_MAX_REQUESTS_TEST = 10     # for testing mode
NYT_DAILY_LIMIT = 500          # alls per day
NYT_RATE_LIMIT_SLEEP = 12      # seconds between API requests (ie. 5/min)
NYT_PAGE_LIMIT = 100          

# Storage
RAW_JSON_DIR = "data/"
PROCESSED_CSV = "data/nyt_ibm_articles.csv"