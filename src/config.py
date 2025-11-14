# NYT CONFIG
from dotenv import load_dotenv
import os
from datetime import datetime

# get api key from .env
load_dotenv()
NYT_API_KEY = os.getenv("NYT_API_KEY")

# 2 years
START_DATE = datetime(2023, 11, 14)
END_DATE = datetime(2025, 11, 13)

# NYT API constraints
NYT_DAILY_LIMIT = 500 # calls per day 
NYT_RATE_LIMIT_SLEEP = 12 # seconds between API requests (ie. 5/min)
NYT_PAGE_LIMIT = 100          

# Storage
RAW_JSON_DIR = "data/"
PROCESSED_CSV = "data/nyt_ibm_articles.csv"