#!/usr/bin/env python3
import argparse, os
import pandas as pd
from indicators import sma, rsi

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--infile", required=True, help="e.g., data/raw/AAPL_2021-01-01_2023-12-31.csv")
    ap.add_argument("--outfile", default=None, help="output path (default: data/processed/<name>_signals.csv)")
    ap.add_argument("--sma_fast", type=int, default=20)
    ap.add_argument("--sma_slow", type=int, default=50)
    ap.add_argument("--rsi_th", type=int, default=55)
    args = ap.parse_args()

    df = pd.read_csv(args.infile, parse_dates=["date"]).set_index("date")
    # 计算指标
    df["sma_fast"] = sma(df["close"], args.sma_fast)
    df["sma_slow"] = sma(df["close"], args.sma_slow)
    df["rsi"] = rsi(df["close"], 14)

    # 生成信号：SMA_fast > SMA_slow 且 RSI > rsi_th → 做多，否则空仓
    df["signal"] = ((df["sma_fast"] > df["sma_slow"]) & (df["rsi"] > args.rsi_th)).astype(int)

    # 保存
    if not args.outfile:
        os.makedirs("data/processed", exist_ok=True)
        base = os.path.basename(args.infile).replace(".csv", "")
        args.outfile = f"data/processed/{base}_signals.csv"

    df.to_csv(args.outfile, index=True)
    print(f"[saved] {args.outfile} rows={len(df)}")

if __name__ == "__main__":
    main()
