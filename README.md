# Description
This project aims to build a machine learning model that predicts IBM’s stock price using Google search interest and sentiment from New York Times (NYT) articles.

# Data Sources
I collected historical IBM stock data using the Ticker.history() method from the yfinance library and saved the resulting DataFrame as a CSV file. 

Also, I obtained article data on IBM from the NYT Article Search API, which returns detailed JSON documents. A typical entry includes fields such as abstract, headline, keywords, pub_date, and web_url, along with relevant metadata about the article’s content and publication context. The New York Times Article Search API allows data to be searched for by keywords and filtered using parameters such as date ranges. It returns structured JSON objects for each article, which include metadata, headlines, abstracts, and publication details.

Finally I collected data of Google search trends using the pytrends library. 


# Results


# Installation
I used a NYT Developer API key for an app to search article data. I set it in an .env file that looks simular to the .env.example file. Please add your API key there to run on your own.

I have used quite a few special python packages. First is yfinance which allows me to pull stock data from Yahoo Finance based on a ticker. Then we have os and dotenvn which allowed me to get my API key accessible. I used pandas to help manage my data in a DataFrame. I used datetime and time to help communcate differnt dates. Finally, I used json to help save my article data.

# Running Analytics 


# Run Instructions 
The project should be run from the src directory. Main.py will run the project and tests.py will run its tests. 
