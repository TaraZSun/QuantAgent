"""Convert CSV stock data files into Parquet format, creating separate Parquet files 
for each stock ticker. The result are 10 parquet files, one for each ticker in the input CSV files."""
import os
import pyarrow.parquet as pq
import logging
import pandas as pd
import pathlib
from pyarrow import Table
from src.const import PARQUET_INPUT_DIR as INPUT_DIR,PARQUET_OUTPUT_DIR as OUTPUT_DIR

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def convert_a_csv_to_parquet(csv_path: pathlib.Path, output_parquet: pathlib.Path) -> None:
    """Convert all CSV files containing stock data into separate Parquet files for each ticker."""
    df = pd.read_csv(csv_path)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for ticker,group in df.groupby("Ticker"):
        output_file = os.path.join(output_parquet, f"{ticker}.parquet")
        table = Table.from_pandas(group)
        pq.write_table(table, output_file)
        logger.info(f"[saved] {output_file}  rows={len(group)}")

def convert_all_csv(input_dir:pathlib.Path, output_parquet: pathlib.Path) -> None:
    """Convert all CSV files in the input directory to Parquet format."""
    input_paths = pathlib.Path(input_dir)
    for csv_file in input_paths.glob("*.csv"):
        convert_a_csv_to_parquet(csv_file, output_parquet)

def main():
    input_path = pathlib.Path(INPUT_DIR)
    output_path = pathlib.Path(OUTPUT_DIR)
    convert_all_csv(input_dir=input_path, output_parquet=output_path)

if __name__ == "__main__":
    main()