## Structured Price Data Pipeline (Yahoo Finance)

This pipeline fetches and prepares **daily OHLCV data** from **Yahoo Finance** for a small
universe of NASDAQ stocks (e.g. 10 tickers) over the period **2010-01-01 to 2023-12-31**.
The data is then converted to Parquet and enriched with technical indicators.

> All commands below are intended to be run from the project root with the virtual
> environment activated.

---

### 1. Fetch raw price data from Yahoo Finance

Download daily OHLCV for the NASDAQ-10 universe:

```bash
python -m src.process_data.structure_data.fetch_yahoo_data
```

This step will:
Read the target tickers from the configured universe file
Fetch daily OHLCV data (Open, High, Low, Close, AdjClose, Volume) from Yahoo Finance
Save the raw files as CSV under the configured data/raw/ directory

### 2. Convert CSV to Parquet
Normalize and convert the raw CSV files to Parquet format:

```bash
python -m src.process_data.structure_data.convert_to_parquet
```
This step will:
Load the CSV files produced in step 1
Ensure consistent column naming (e.g. Date, Ticker, Open, High, Low, Close, AdjClose, Volume)
Write cleaned data as Parquet files (e.g. under data/clean/price_daily_parquet/)

### 3. Create technical features (10+ indicators)
Compute a first set of technical indicators based on OHLCV and save them as Parquet
for efficient downstream use:

```bash
python -m src.process_data.structure_data.create_features.features
```
This step will:
Load the daily OHLCV Parquet files from step 2
Compute at least 10 technical indicators (e.g. SMA, EMA, RSI, MACD, ATR, Bollinger Bands)
Save the enriched feature tables as Parquet files (e.g. under data/features_10/)
for later use in modeling and backtesting

