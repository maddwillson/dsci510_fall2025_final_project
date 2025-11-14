from load import load_yf_data
import pandas as pd
import yfinance as yf

if __name__ == "__main__":

    print("YFINANCE LOAD TESTS...")

    print("\nTest: Load Data")
    try:
        yf_df = load_yf_data("IBM", "1mo")
        if isinstance(yf_df, pd.DataFrame) and not yf_df.empty:
            print("\n[PASS] Data loaded")
        else:
            print("\n[FAIL] Data not loaded correctly")
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        

    print("\nTest: Check for Date column")
    try:
        load_yf_data()
        if "Date" in yf_df.columns:
            print("\n[PASS] Date column exists\n")
        else:
            print("\n[FAIL] Date column missing\n")
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}\n")


    print("\nTest: Invalid ticker")
    try:
        load_yf_data("NOT A TICKER", "1mo")
        print("\n[FAIL] Expected ValueError ")
    except Exception as e:
        print("\n[PASS] Correctly raised: {e}")
    
