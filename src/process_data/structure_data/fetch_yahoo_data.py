"""Script to fetch 10 companies historical stock data within NASDAQ-100 using yfinance 
    and save to CSV files.
result looks like:
Date,Ticker,Open,High,Low,Close,AdjClose,Volume,Dividends,StockSplits
2010-01-04,AAPL,30.49,30.64,30.34,30.57,27.727419,123432400,0.0,0.0
"""

import os
import pandas
import yfinance 
import pathlib
import logging

from src.const import CSV_FILE, START_DATE, END_DATE, OUTPUT_DIR
logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def fetch_raw_data(csv_file: pathlib.Path) -> pandas.DataFrame:
    """Fetch raw stock data from yfinance for tickers listed in the given CSV file."""
    tickers = pandas.read_csv(csv_file)["Symbol"].dropna().tolist()
    data = yfinance.download(
        tickers=tickers,
        start=START_DATE,
        end=END_DATE,
        interval="1d",
        group_by="columns",
        actions=True,
        auto_adjust=False,
    )
    return data

def convert_raw_data(data: pandas.DataFrame) -> pandas.DataFrame:
    """Convert a yfinance multi-level column DataFrame into a two-dimensional long table."""
    if isinstance(data.columns, pandas.MultiIndex):
        level0 = data.columns.get_level_values(0)
        wanted_fields = {"Open", "High", "Low", "Close", "Adj Close","Volume","Dividends","Stock Splits"}
        if wanted_fields.isdisjoint(set(level0)):
            data.columns=data.columns.swaplevel(0,1)
            data = data.sort_index(axis=1)
    else:
        raise ValueError("Input data must have MultiIndex columns.")
    existing_columns = [c for c in ["Open", "High", "Low", "Close", "Adj Close","Volume","Dividends","Stock Splits"]
                         if c in data.columns.get_level_values(0)]
    data = data[existing_columns]
    df =data.stack(level=1).reset_index()
    if "Date" not in df.columns:
        df = df.rename(columns={"index":"Date","level_0": "Date"})
    df = df.rename(
        columns={
            "level_1": "Ticker",
            "Adj Close": "AdjClose",
            "Stock Splits": "StockSplits",
        },
    )
    wanted_cols = ["Date", "Ticker", "Open", "High", "Low", "Close",
               "AdjClose", "Volume", "Dividends", "StockSplits"]
    df = df[wanted_cols]
    df["Date"] = pandas.to_datetime(df["Date"]).dt.date
    df = df.sort_values(by=["Ticker", "Date"])
    return df

def save_data_to_csv(df: pandas.DataFrame, output_dir: pathlib.Path)-> None:
    """Save the DataFrame into separate CSV files for each ticker."""
    os.makedirs(output_dir, exist_ok=True)
    tickers = df["Ticker"].unique()
    for ticker in tickers:
        df_ticker = df[df["Ticker"] == ticker]
        output_file = output_dir / f"{ticker}_{START_DATE}_{END_DATE}.csv"
        df_ticker.to_csv(output_file, index=False)
       

def main():
    csv_path = pathlib.Path(CSV_FILE)
    output_path = pathlib.Path(OUTPUT_DIR)
    raw_data = fetch_raw_data(csv_path)
    converted_data = convert_raw_data(raw_data)
    save_data_to_csv(converted_data, output_path)
    logger.info(f"Data saved to {output_path}")


if __name__ == "__main__":
    main()



