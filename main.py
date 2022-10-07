import requests
from twilio.rest import Client
import os

MY_PHONE_NUMBER = os.environ.get("MY_PHONE_NUMBER")

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

#Twilio account details
ACCOUNT_SID = os.environ.get("TWILIO_ACC_SID")   
AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")     

stock_parameters = {
    "function"  : "TIME_SERIES_DAILY",
    "symbol"    : STOCK_NAME,
    "apikey"    : STOCK_API_KEY,
}

news_parameters = {
    "q"         : COMPANY_NAME,
    "apiKey"    : NEWS_API_KEY,
}

# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
data = stock_response.json()

time_series_daily = data["Time Series (Daily)"]
# get closing stock prices for all days
closing_stock_price_day = [stock_data["4. close"] for (date, stock_data) in time_series_daily.items()]
# get yesterday's closing stock price
yesterday_closing_sp = float(closing_stock_price_day[0])

# Get the day before yesterday's closing stock price
day_before_yest_sp = float(closing_stock_price_day[1])

# Find the difference between 1 and 2
sp_differece = yesterday_closing_sp - day_before_yest_sp
arrow_emoji = None
if sp_differece > 0:
    arrow_emoji = "🔺"
else:
    arrow_emoji = "🔻"

# Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
pc_difference = round((sp_differece / yesterday_closing_sp) * 100)

# If percentage is greater than 5 
if pc_difference > 5:
    # get the first 3 news pieces for the COMPANY_NAME. 
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()
    # create list for articles
    articles = [article for article in news_data["articles"]]
    news_pieces = articles[:3]  # get first 3 news pieces
    
    # Use twilio.com
    # to send a seperate message with each article's title and description to your phone number. 
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    
    for index in  range(len(news_pieces)):
        message = client.messages.create(body=f"{STOCK_NAME}: {arrow_emoji}{pc_difference}\n \
                                        Headline: {news_pieces[index]['title']}:\n \
                                        Brief: {news_pieces[index]['description']}",
                                        from_="+16292763317",
                                        to=MY_PHONE_NUMBER
                                        )
    print(message.status) 

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

