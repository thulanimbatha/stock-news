import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_api_key = "1D85KWEBOZIW7989"
news_api_key = "d04f83c61d834f06b3deb18b20e08063"

account_sid ="ACfa486f58e390aaf8fdb12578a32fd640"   #Twilio account details
auth_token = "5c4bfa87d74f879c4e903769bfa328fa"     #Twilio account details

stock_parameters = {
    "function"  : "TIME_SERIES_DAILY",
    "symbol"    : "IBM",
    "apikey"    : stock_api_key,
}

news_parameters = {
    "q"         : COMPANY_NAME,
    "apiKey"    : news_api_key,
}

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

stock_response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
data = stock_response.json()

time_series_daily = data["Time Series (Daily)"]
# get closing stock prices for all days
closing_stock_price_day = [stock_data["4. close"] for (date, stock_data) in time_series_daily.items()]
# get yesterday's closing stock price
yesterday_closing_sp = float(closing_stock_price_day[0])

#TODO 2. - Get the day before yesterday's closing stock price
day_before_yest_sp = float(closing_stock_price_day[1])

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
sp_differece = abs(yesterday_closing_sp - day_before_yest_sp)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
pc_difference = (sp_differece / yesterday_closing_sp) * 100

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if pc_difference > 5:
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()
    # create list for articles
    articles = [article for article in news_data["articles"]]
    news_pieces = articles[:3]  # get first 3 news pieces
    
#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 
    client = Client(account_sid, auth_token)
    
    message = client.messages.create(body=f"{news_pieces[0]['title']}:\n{news_pieces[0]['description']}\
                                    \n\n{news_pieces[1]['title']}:\n{news_pieces[1]['description']}\
                                    \n\n{news_pieces[2]['title']}:\n{news_pieces[2]['description']}",
                                    from_="+16292763317",
                                    to="+27834158673"
                                    )

    print(message.status)

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#TODO 9. - Send each article as a separate message via Twilio. 



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

