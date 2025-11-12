import os
# Fetch_data.py
CSV_FILE = "data/raw/nasdaq10_tickers.csv"
START_DATE = "2010-01-01"
END_DATE = "2023-12-31"
OUTPUT_DIR = "data/price_daily"

# convert_to_parquet.py
PARQUET_OUTPUT_DIR = "data/clean/price_daily_parquet"
PARQUET_INPUT_DIR = "data/price_daily"

