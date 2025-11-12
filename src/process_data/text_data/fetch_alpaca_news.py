# This module fetches news data from the Alpaca News API within a specified date range.
# Please make sure you have the required environment variables set for API access.
import datetime
import requests
import os
from dotenv import load_dotenv
# from src.process_data.const import START_DATE, END_DATE
load_dotenv()

START_DATE = "2010-01-01"
END_DATE = "2023-12-31"
# ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
# ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")
# ALPACA_NEWS_API_URL = os.getenv("ALPACA_NEWS_API_URL")  # e.g., https://data.alpaca.markets/v1/news 
# ALPACA_ENDPOINT = os.getenv("ALPACA_NEWS_API_ENDPOINT")

ALPACA_NEWS_API_URL  = os.getenv("ALPACA_NEWS_API_URL", "https://data.alpaca.markets/v1beta1/news")
ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID") or os.getenv("ALPACA_API_KEY")
ALPACA_API_SECRET = os.getenv("APCA_API_SECRET_KEY") or os.getenv("ALPACA_API_SECRET")

def load_tickers(filepath: str) -> list[str]:
    with open(filepath, 'r') as file:
        tickers = [line.strip() for line in file if line.strip()]
    return tickers

def fetch_alpaca_news(start_date: datetime.date, end_date: datetime.date, tickers:list[str]) -> list[dict]:
    if not ALPACA_API_KEY or not ALPACA_API_SECRET:
        raise ValueError("Alpaca API credentials are not set in environment variables.")
    headers = {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_API_SECRET
    }
    
    params = {
        "start": f"{start_date}T00:00:00Z",
        "end": f"{end_date}T23:59:59Z",
        "limit": 50,
        "sort": "asc",
    }

    response = requests.get(ALPACA_NEWS_API_URL, headers=headers, params=params)
    response.raise_for_status()

    news_items = response.json()
    return news_items

result = fetch_alpaca_news(datetime.date.fromisoformat(START_DATE), datetime.date.fromisoformat(END_DATE))
print(f"Fetched {len(result)} news items from Alpaca News API.")