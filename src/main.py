from load import load_yf_data
import pandas as pd
import yfinance as yf


if __name__ == "__main__":
    # YFINANCE
    yf_df = load_yf_data()

    #download if needed
    #yf_df.to_csv("yf_df.csv", index=False)


