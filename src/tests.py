import pandas as pd
from datetime import datetime
from pathlib import Path

from src.load.load_stock import load_yf_data
from src.load.load_articles import load_nyt_data
from src.load.load_trends import load_google_data

from src.process.clean_articles import clean_articles, load_articles_json
from src.process.clean_stock import clean_stock_data, load_stock_data_csv
from src.process.clean_trends import clean_trends_data, load_trends_csv
from src.process.merge_data import merge_data
from src.process.sentiment_analysis import compute_sentiments

from analyze.eda import eda, data_path, variables
from analyze.modeling import modeling

def load_tests():
    
    ##### YFINANCE
    print("YFINANCE LOAD TESTS...")

    Y_START = "20250101"
    Y_END = "20250201"

    print("\nTest: Load Data")
    try:
        yf_df = load_yf_data(start_date=Y_START, end_date=Y_END, ticker="IBM")
        if isinstance(yf_df, pd.DataFrame) and not yf_df.empty:
            print("\n[PASS] Data loaded")
        else:
            print("\n[FAIL] Data not loaded correctly")
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")

    print("\nTest: Invalid ticker")
    try:
        load_yf_data(start_date=Y_START, end_date=Y_END, ticker="NOT_A_REAL_TICKER")
        print("\n[FAIL] Expected ValueError ")
    except Exception as e:
        print(f"\n[PASS] Correctly raised: {e}")
    

    ##### GOOGLE
    print("\nGOOGLE TRENDS LOAD TESTS...")

    G_START = "2025-01-01"
    G_END = "2025-02-01"

    print("\nTest: Load Google Trends data")
    try:
        google_df = load_google_data(["IBM"], start_date=G_START, end_date=G_END)
        if isinstance(google_df, pd.DataFrame) and not google_df.empty:
            print("\n[PASS] Google Trends data loaded")
        else:
            print("\n[FAIL] Google returned empty data")
    except Exception as e:
        print(f"\n[FAIL] Google Trends error: {e}")

    
    ##### NYT
    print("\nNYT API LOAD TEST...")

    # should find 12 articles in this range:
    N_START, N_END= "20250109", "20250310"
    articles = None

    try: 
        articles = load_nyt_data(
            query="IBM",
            start_date=N_START,
            end_date=N_END,
            max_requests=2,        
        )
        if len(articles) == 12:
            print(f"[PASS] All Expected articles returned")
        elif len(articles) > 0:
            print(f"[FAIL] Expected 12 but {len(articles)} articles were returned")
        else:
            print("[FAIL] No articles returned.")
    except Exception as e:
        raise RuntimeError(f"[FAIL] Failed NYT API test: {e}")








  
def clean_tests():

    print("CLEANING TESTS...")

    DATA_ROOT = Path(__file__).parents[1] / "data"

    ##### YFINANCE
    print("\nYFINANCE CLEANING TESTS...")

    raw_yf = DATA_ROOT / "raw" / "yf_df.csv"
    try:
        df = clean_stock_data(raw_yf)
        if isinstance(df, pd.DataFrame) and not df.empty:
            print("[PASS] Stock clean function returns valid DataFrame")
        else:
            print("[FAIL] Stock clean returned empty or invalid dataframe")
    except Exception as e:
        print(f"[FAIL] Stock clean error: {e}")


    ##### GOOGLE
    print("\nGOOGLE TRENDS CLEANING TESTS...")

    raw_google = DATA_ROOT / "raw" / "google_df.csv"
    try:
        df = clean_trends_data(raw_google)
        if isinstance(df, pd.DataFrame) and not df.empty:
            print("[PASS] Google Trends clean returned valid DataFrame")
        else:
            print("[FAIL] Google Trends clean returned empty/invalid DataFrame")
    except Exception as e:
        print(f"[FAIL] Google Trends clean error: {e}")


    ##### NYT 
    print("\nNYT ARTICLE CLEANING TESTS...")

    raw_nyt = DATA_ROOT / "raw" / "nyt_data.json"
    try:
        df = clean_articles(raw_nyt)
        if isinstance(df, pd.DataFrame) and not df.empty:
            print("[PASS] NYT articles cleaned successfully")
        else:
            print("[FAIL] empty/invalid DataFrame was returned")
    except Exception as e:
        print(f"[FAIL] clean NYT error: {e}")







def sentiment_tests():
    print("SENTIMENT ANALYSIS TESTS...")

    DATA_ROOT = Path(__file__).parents[1] / "data" / "processed"
    sentiment_input = DATA_ROOT / "nyt_clean.csv"

    print("\nTest: Compute sentiment from cleaned NYT articles")
    try:
        df = compute_sentiments(nyt_clean_path=str(sentiment_input))

        if isinstance(df, pd.DataFrame) and not df.empty:
            print("[PASS] Sentiment function returned DataFrame")
        else:
            print("[FAIL] Sentiment function returned empty or invalid DataFrame")
            return
    except Exception as e:
        print(f"[FAIL] Sentiment function raised unexpected error: {e}")
        return

    print("\nTest: Required columns exist")
    required_cols = {"Date", "Sentiment", "Prev_sentiment"}

    if required_cols.issubset(df.columns):
        print("[PASS] All required sentiment columns present")
    else:
        missing = required_cols - set(df.columns)
        print(f"[FAIL] Missing sentiment columns: {missing}")

    print("\nTest: Sentiment values computed")
    if df["Sentiment"].notna().any():
        print("[PASS] Sentiment column contains valid values")
    else:
        print("[FAIL] All Sentiment values are NaN — check input headlines")


    print("\nTest: No crashes on invalid headline values (None, NaN)")
    try:
        temp_df = pd.DataFrame({
            "Date": pd.to_datetime(["2025-01-01", "2025-01-02"]),
            "Headline": [None, "IBM reports strong earnings"]
        })
        temp_path = DATA_ROOT / "_temp_test_headlines.csv"
        temp_df.to_csv(temp_path, index=False)

        _ = compute_sentiments(nyt_clean_path=str(temp_path))
        print("[PASS] Function handles None/NaN headlines safely")

        temp_path.unlink(missing_ok=True)
    except Exception as e:
        print(f"[FAIL] Crashed on invalid headline values: {e}")









def merge_tests():
    print("MERGE DATA TESTS...")

    DATA_ROOT = Path(__file__).parents[1] / "data" / "processed"

    yf_path = DATA_ROOT / "yf_clean.csv"
    google_path = DATA_ROOT / "google_clean.csv"
    nyt_path = DATA_ROOT / "nyt_sentiments.csv"

    print("\nTest: Merge function returns DataFrame")
    try:
        merged = merge_data()

        if isinstance(merged, pd.DataFrame) and not merged.empty:
            print("[PASS] merge_data returned valid DataFrame")
        else:
            print("[FAIL] merge_data returned empty or invalid DataFrame")
            return

    except Exception as e:
        print(f"[FAIL] merge_data raised an unexpected error: {e}")
        return


    print("\nTest: No null values after merge")
    if merged.isna().sum().sum() == 0:
        print("[PASS] No NaN values remain in merged dataset")
    else:
        print("[FAIL] Found NaN values after merge")


    print("\nTest: Columns from all sources are present")
    # load a sample row from each source to inspect columns
    yf_cols = pd.read_csv(yf_path, nrows=1).columns
    google_cols = pd.read_csv(google_path, nrows=1).columns
    nyt_cols = pd.read_csv(nyt_path, nrows=1).columns

    # merged df columns
    merged_cols = set(merged.columns)

    # we expect all except the duplicate Date columns
    expected_cols = set(yf_cols) | set(google_cols) | set(nyt_cols)

    # Date will appear only once in merged_df
    expected_cols = expected_cols - {"Date"}
    merged_cols_no_date = merged_cols - {"Date"}

    if expected_cols.issubset(merged_cols_no_date):
        print("[PASS] All expected columns were merged")
    else:
        missing = expected_cols - merged_cols_no_date
        print(f"[FAIL] Missing expected columns in merged dataset: {missing}")






def analyze_tests():
    ##### EDA
    print("EDA TESTS...")


    print("\nTest: EDA function runs without crashing")
    try:
        figs = eda()
        print("[PASS] EDA ran successfully")
    except Exception as e:
        print(f"[FAIL] EDA raised an error: {e}")
        return

    print("\nTest: EDA returned dictionary of figures")
    if isinstance(figs, dict) and len(figs) > 0:
        print("[PASS] EDA returneds a populated dict")
    else:
        print("[FAIL] EDA did not return a populated dict")
        return

    required_keys = [
        "variable_distributions",
        "corr_heatmap",
        "interest_sentiment_scatter",
        "return_by_dayofweek",
        "pairplot",
        "time_series",
    ]

    print("\nTest: All expected figure keys exist")
    missing = [k for k in required_keys if k not in figs]
    if not missing:
        print("[PASS] All expected figures produced")
    else:
        print(f"[FAIL] Missing figure keys: {missing}")





    ##### MODELING
    print("MODELING TESTS...")

    data_path = Path(__file__).parents[1] / "data" / "final" / "ibm_df.csv"

    print("\nTest: Final IBM dataset exists")
    if not data_path.exists():
        print(f"[FAIL] Missing dataset: {data_path}")
        return
    else:
        print("[PASS] Found dataset for modeling")

    print("\nTest: Modeling function runs without crashing")
    try:
        results_df, fig = modeling()
        print("[PASS] Modeling ran successfully")
    except Exception as e:
        print(f"[FAIL] modeling() raised an error: {e}")
        return



    print("\nTest: Modeling returned valid results_df and fig")
    import matplotlib.figure
    if isinstance(results_df, pd.DataFrame) and not results_df.empty:
        print("[PASS] results_df is a valid DataFrame")
    else:
        print("[FAIL] Invalid or empty results_df")

    if isinstance(fig, matplotlib.figure.Figure):
        print("[PASS] Modeling returned a valid Matplotlib Figure")
    else:
        print("[FAIL] Figure returned by modeling() is invalid")


    print("\nTest: Expected models ran")
    expected_models = {
        "Logistic Regression",
        "Ridge Classifier",
        "Naive Bayes",
        "KNN Classifier",
    }

    if "Model" not in results_df.columns:
        print("[FAIL] results_df missing 'Model' column")
    else:
        models_found = set(results_df["Model"])
        missing_models = expected_models - models_found
        if not missing_models:
            print("[PASS] All expected models found in results")
        else:
            print(f"[FAIL] Missing models in results_df: {missing_models}")










if __name__ == "__main__":
    print("\nTesting data loading...")
    load_tests()

    print("\nTesting data cleaning...")   
    clean_tests()
    
    print("\nTesting sentiment analysis...")  
    sentiment_tests()

    print("\nTesting data merging...")  
    merge_tests()

    print("\nTesting data analysis...")  
    analyze_tests()

    print("\nDone with testing!")