from twilio.rest import Client
import requests
from dotenv import load_dotenv
import os

load_dotenv("C:/Users/Moham/PycharmProjects/Environment_Variables/.env")

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ALPHA_KEY = os.getenv("alpha_key")
NEWS_KEY = os.getenv("news_key")

TWILIO_SID = os.getenv("account_sid")
TWILIO_AUTH = os.getenv("auth_token")

personal_number = os.getenv("personal_phone_no")

alpha_parameters = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "outputsize": "compact",
    "datatype": "json",
    "apikey": ALPHA_KEY
}

alpha_response = requests.get(url="https://www.alphavantage.co/query", params=alpha_parameters)
alpha_response.raise_for_status()
alpha_data = alpha_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in alpha_data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

day_before_yesterday = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday["4. close"]

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)

up_down = None
if difference < 0:
    up_down = "🔻"
else:
    up_down = "🔺"

percentage_diff = round((difference / float(yesterday_closing_price)) * 100)

if abs(percentage_diff) > 5:
    news_params = {
        "apikey": NEWS_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]

    three_articles = news_data[:3]

    formatted_articles = [f"{STOCK}: {up_down}{percentage_diff}%\nHeadline: {article['title']} Brief: {article['description']}" for article in three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH)

    for article in formatted_articles:

        message = client.messages \
            .create(
            body = article,
            from_= '+13393310995',
            to = personal_number
        )

