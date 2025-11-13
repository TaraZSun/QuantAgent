# create 10 features for trial, more can be added later
import pandas as pd
import pandas_ta as ta
from src.const import FEATURES_INPUT_DIR
import pathlib
import logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def compute_features_10(df: pd.DataFrame) ->pd.DataFrame:
    data = df.copy()
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.sort_values(["Ticker","Date"]).reset_index(drop=True)

    def _one(group: pd.DataFrame) ->pd.DataFrame:
        o=group["Open"]
        h=group["High"]
        l=group["Low"]
        c=group["Close"]
        v=group["Volume"]

        out = pd.DataFrame(index=group.index)

        # 10 indicators
        out=out.join(ta.sma(c, length=20).to_frame("feat_sma_20"), how="outer")
        out = out.join(ta.sma(c, length=50).to_frame(name="feat_sma50"), how="outer")
        out = out.join(ta.ema(c, length=20).to_frame(name="feat_ema20"), how="outer")
        out = out.join(ta.rsi(c, length=14).to_frame(name="feat_rsi14"), how="outer")
        out = out.join(ta.macd(c, fast=12, slow=26, signal=9).add_prefix("feat_macd_"), how="outer")
        out = out.join(ta.atr(h, l, c, length=14).to_frame(name="feat_atr14"), how="outer")
        out = out.join(ta.bbands(c, length=20).add_prefix("feat_bb20_"), how="outer")
        out = out.join(ta.adx(h, l, c, length=14).add_prefix("feat_adx14_"), how="outer")
        out = out.join(ta.mfi(h, l, c, v, length=14).to_frame(name="feat_mfi14"), how="outer")
        out = out.join(ta.obv(c, v).to_frame(name="feat_obv"), how="outer")

        out = out.shift(1)  # avoid lookahead bias
        return pd.concat([group.reset_index(drop=True), out.reset_index(drop=True)], axis=1)
    return  data.groupby("Ticker", group_keys=False).apply(_one, include_groups=False)

def create_features_for_all_companies(input_dir:pathlib.Path)->None:
    output_dir = input_dir.parent / "features_10"
    output_dir.mkdir(exist_ok=True)
    for file in input_dir.glob("*.parquet"):
        df = pd.read_parquet(file)
        df_feat = compute_features_10(df)
        output_file = output_dir / file.name
        df_feat.to_parquet(output_file)
    logger.info("Features creation completed.")

def main():
    input_dir = pathlib.Path(FEATURES_INPUT_DIR)
    print(input_dir)
    create_features_for_all_companies(input_dir)
    

if __name__ == "__main__":
    main()
