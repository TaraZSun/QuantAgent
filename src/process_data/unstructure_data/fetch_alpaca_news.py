# This module fetches news data from the Alpaca News API within a specified date range.
# Please make sure you have the required environment variables set for API access.
import datetime
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import hashlib
import json
import os
import pathlib
import pandas as pd
from src.const import START_DATE, END_DATE, MAX_RETRIES, TIMEOUT, TICKERS_FILE_PATH, TICKERS_OUTPUT_PATH
from src.process_data.unstructure_data.models import EntityNewsRaw
from dotenv import load_dotenv
load_dotenv()

ALPACA_NEWS_API_URL  = os.getenv("ALPACA_NEWS_API_URL")
ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID") or os.getenv("ALPACA_API_KEY")
ALPACA_API_SECRET = os.getenv("APCA_API_SECRET_KEY") or os.getenv("ALPACA_API_SECRET")

@retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_fixed(2),reraise=True
            )
def call_alpaca_news_api(start_date: datetime.date, 
                        end_date: datetime.date, 
                        ticker: str, 
                        page_token:str | None) -> dict:
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
        "symbols": ticker
    }
    if page_token:
        params["page_token"] = page_token
    response = requests.get(ALPACA_NEWS_API_URL, headers=headers, params=params, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_news_for_ticker(ticker: str) -> list[EntityNewsRaw]:
    ticker = ticker.upper().strip()
    items: list[EntityNewsRaw] = []
    start_date = datetime.date.fromisoformat(START_DATE)
    end_date = datetime.date.fromisoformat(END_DATE)
    next_token: str | None = None

    try:
        while True:
            data = call_alpaca_news_api(start_date, end_date, ticker, next_token)
            batch = data.get("news", [])
            for raw in batch:
                ts_str = (
                    raw.get("created_at") or
                    raw.get("published_utc") or
                    raw.get("updated_at") or
                    raw.get("published_at")
                )
                if not ts_str:
                    continue

                ts = pd.to_datetime(ts_str, utc=True)   
                url = raw.get("url") or None
                news_id = hashlib.sha1(f"{ticker}|{ts.isoformat()}|{url or ''}".encode('utf-8')).hexdigest()  
                model = EntityNewsRaw(
                    news_id=news_id,
                    Ticker=ticker,
                    published_at_utc=ts.to_pydatetime(),
                    source=raw.get("source"),
                    url=url,
                    headline=raw.get("headline"),
                    summary=raw.get("summary"),
                    category=raw.get("category"),
                    language=raw.get("language"),
                )
                items.append(model)
            next_token = data.get("next_page_token")
            if not next_token:
                break
    except requests.HTTPError as e:
        print(f"HTTP error occurred while fetching news for {ticker}: {e}")

    return items
    
    
def save_news_for_ticker(news_items: list[EntityNewsRaw], ticker: str, output_dir: pathlib.Path) -> None:
    if not news_items:
        print(f"No news items found for ticker {ticker}.")
        return
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{ticker}_news_raw.json"
    with open(output_file.with_suffix('.json'), 'w') as f:
        json.dump([news_item.model_dump(mode="json") for news_item in news_items], 
                  f, indent=2, ensure_ascii=False)

def save_news_for_tickers(tickers_file_path: pathlib.Path) -> None:
    tickers = pd.read_csv(tickers_file_path)["Symbol"].tolist()
    output_dir = pathlib.Path(TICKERS_OUTPUT_PATH)
    for ticker in tickers:
        news_items = get_news_for_ticker(ticker)
        save_news_for_ticker(news_items, ticker, output_dir)

def main():
    tickers_file = pathlib.Path(TICKERS_FILE_PATH)
    save_news_for_tickers(tickers_file)

if __name__ == "__main__":
    main()


