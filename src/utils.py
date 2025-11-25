from pathlib import Path
import pandas as pd
from datetime import datetime


# Directory helper
def ensure_parent_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


# Date conversion helpers:
def yyyymmdd_to_datetime(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y%m%d")


def to_ymd(date_obj: datetime) -> str:
    return date_obj.strftime("%Y-%m-%d")


def ymd_to_dash(date_str: str) -> str:
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"


# CSV helper
def save_csv(df: pd.DataFrame, path: str):
    ensure_parent_dir(path)
    df.to_csv(path, index=False)


# Figure helper
def save_fig(fig, path: str):
    ensure_parent_dir(path)
    fig.savefig(path)
