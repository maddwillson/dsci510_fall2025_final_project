from dotenv import load_dotenv
import os
from datetime import datetime



# DATE CONFIG (past 5 years)
TODAY = datetime.today()
START_DATE = datetime(TODAY.year - 5, TODAY.month, TODAY.day).strftime("%Y%m%d")
END_DATE = TODAY.strftime("%Y%m%d")


## NYT CONFIG
load_dotenv()
NYT_API_KEY = os.getenv("NYT_API_KEY")

# NYT API constraints
NYT_DAILY_LIMIT = 500 # calls per day 
NYT_RATE_LIMIT_SLEEP = 12 # seconds between API requests (ie. 5/min)
NYT_PAGE_LIMIT = 100 