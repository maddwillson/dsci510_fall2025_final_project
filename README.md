# Description
This project aims to build a machine learning model that predicts IBM’s stock price movement using three main data sources: historical IBM stock prices, public interest proxied by Google search volumes, and public sentiment proxied by New York Times (NYT) article headlines. The overall goal is to use 5 years of public attention and tone to help explain or predict short term returns in IBM’s stock performance.

# Data Sources
I collected IBM stock price data using the Ticker.history() method from the yfinance library, which gets historical data from Yahoo Finance. I processed 1256 raw rows as a DataFrame and saved them as a CSV file. The raw dataset includes daily stock price open, high, low, close, return and volume values for IBM stock.

I also obtained article data from the NYT Article Search API. This API returned 596 JSON structured articles. The data included fields such as the abstract, headline, publication date, snippit, and web_url. I used these responses to gather several years of NYT coverage mentioning IBM. Articles were saved in raw JSON format before being cleaned via a DataFrame and saved into a CSV file. For this data source alone, I also performed sentiment analysis and found that analysis of the headline made the most sense for downstream use.

Finally, I collected 1827 rows of Google Trends data for the keyword “IBM” using the pytrends library. Since Google Trends restricts daily resolution data to 270 day windows, I pulled the data in multiple chunks and stitched them together. I processed the data as a DataFrame and saved it as a CSV file. The data in the raw file included two feilds: date and IBM search interest, scaled from 1 to 100 for a given time period.

# Results
After cleaning and preparing all datasets, I merged stock features (like returns, rolling windows, and volatility), Google search interest, and NYT sentiment into a single unified dataset.
I then trained several machine learning models—including Logistic Regression, Ridge Classifier, Gaussian Naive Bayes, and K-Nearest Neighbors—to predict whether IBM’s stock would move up by more than 0.5% the following day.
Model performance was evaluated using accuracy, F1-scores, and confusion matrices, and all results are plotted and saved in the results directory.

# Installation
I used an NYT Developer API key to access article data. It should be placed in an .env file similar to the provided .env.example. Please add your API key there to run the data loading pipeline on your own.

Below are the main Python packages I used:

yfinance — pull IBM stock data from Yahoo Finance
pytrends — pull Google search interest data
requests — support API calls for the NYT data
pandas — process my tabular data
numpy — numeric operations throughout
dotenv - load environment varibales 
os — load environment variables
datetime — handle time series data and date formatting 
time - real time rate limit delays
json — read raw NYT article responses
scikit-learn — supports modeling
matplotlib — data visualiztion
seaborn - data visualiztion
pathlib - file path help
vaderSentiment - Sentiment Analysis

# Running Analytics 
No need to change anything when runninging results.ipynb, eda.py or modeling.py files. Everything will be printed or added to a results folder. 

# Run Instructions 
The project should be run from the main Project directory. Within that, src/main.py will run the project and src/tests.py will run its tests. 
