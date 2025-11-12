# validate_and_dump.py
from models import EntityNewsRaw
import pandas as pd
from pydantic import BaseModel

def to_dataframe(objs: list[BaseModel]) -> pd.DataFrame:
    return pd.DataFrame([o.model_dump() for o in objs])

raw_items = [
    {"news_id":"n1","Ticker":"AAPL","published_at_utc":"2019-06-01T14:30:00Z",
     "headline":"Apple launches ...","url":"https://...","source":"Reuters"}
]
valid = [EntityNewsRaw.model_validate(item) for item in raw_items]
df = to_dataframe(valid)
df.to_parquet("data/news/raw/entity_news_raw.parquet", index=False)
