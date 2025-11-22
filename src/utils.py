from datetime import datetime

def yyyymmdd_to_ymd(date_str: str) -> str:
    #YYYYMMDD → YYYY-MM-DD

    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"

def today_str_yyyymmdd() -> str:
    #today's date as YYYYMMDD
    return datetime.today().strftime("%Y%m%d")

def years_ago_str_yyyymmdd(years: int) -> str:
    #Return date N years ago from today as YYYYMMDD
    today = datetime.today()
    return datetime(today.year - years, today.month, today.day).strftime("%Y%m%d")
