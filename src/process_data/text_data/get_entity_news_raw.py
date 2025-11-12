# Script to extract textual data from a dataset of documents from Alpaca news API from 2010-2023 

import json
import hashlib
import pathlib
import pandas as pd

RAW_COLS = ["news_id","Ticker","published_at_utc","source","url",
            "headline","summary","category","language","raw_json"]

def build_entity_news_raw_from_items(items: list[dict]) -> pd.DataFrame:
    records = []
    for item in items:
        news_id = hashlib.sha1(json.dumps(item, sort_keys=True).encode('utf-8')).hexdigest()
        record = {
            "news_id": news_id,
            "Ticker": item.get("ticker", ""),
            "published_at_utc": item.get("published_utc", ""),
            "source": item.get("source", ""),
            "url": item.get("url", ""),
            "headline": item.get("headline", ""),
            "summary": item.get("summary", ""),
            "category": item.get("category", ""),
            "language": item.get("language", ""),
            "raw_json": json.dumps(item)
        }
        records.append(record)
    df = pd.DataFrame.from_records(records, columns=RAW_COLS)
    return df

build_entity_news_raw_from_items(items)