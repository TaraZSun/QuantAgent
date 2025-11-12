# models.py
from datetime import datetime, date
from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional

class EntityNewsRaw(BaseModel):
    news_id: str
    Ticker: str = Field(min_length=1, max_length=10)
    published_at_utc: datetime 
    source: Optional[str] = None
    url: Optional[HttpUrl] = None
    headline: str
    summary: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = None

    @field_validator("published_at_utc")
    @classmethod
    def must_be_utc(cls, v: datetime):
        if not (v.tzinfo and v.utcoffset() == 0):
            raise ValueError("published_at_utc must be timezone-aware UTC")
        return v

class MacroNewsRaw(BaseModel):
    macro_id: str
    published_at_utc: datetime
    source: Optional[str] = None
    url: Optional[HttpUrl] = None
    headline: str
    summary: Optional[str] = None
    topic: Optional[str] = None
    language: Optional[str] = None

    @field_validator("published_at_utc")
    @classmethod
    def must_be_utc(cls, v: datetime):
        if not (v.tzinfo and v.utcoffset() == 0):
            raise ValueError("published_at_utc must be timezone-aware UTC")
        return v

class EntityNewsDaily(BaseModel):
    Ticker: str
    Date: date
    news_cnt: Optional[int] = Field(default=None, ge=0)
    sent_mean: Optional[float] = None
    sent_sum: Optional[float] = None
    pos_sum: Optional[float] = None
    neg_sum: Optional[float] = None


class MacroNewsDaily(BaseModel):
    Date: date
    macro_cnt: Optional[int] = Field(default=None, ge=0)
    macro_sent_mean: Optional[float] = None
    macro_sent_sum: Optional[float] = None
    macro_pos_sum: Optional[float] = None
    macro_neg_sum: Optional[float] = None
