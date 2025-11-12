#!/usr/bin/env python3
import argparse, os, json
import pandas as pd
import matplotlib.pyplot as plt
from backtest import backtest_long_only

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--signals", required=True, help="data/processed/..._signals.csv")
    ap.add_argument("--cash", type=float, default=100000)
    ap.add_argument("--plot", type=int, default=1)
    args = ap.parse_args()

    df = pd.read_csv(args.signals, parse_dates=["date"]).set_index("date")
    res = backtest_long_only(df["close"], df["signal"], cash=args.cash)

    os.makedirs("results/outputs", exist_ok=True)
    # 保存指标
    summary = {k: v for k, v in res.items() if k not in ("equity","daily_returns")}
    with open("results/outputs/summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # 保存权益曲线
    res["equity"].to_csv("results/outputs/equity_curve.csv")
    if args.plot:
        plt.figure(figsize=(8,4))
        res["equity"].plot()
        plt.title("Equity Curve")
        plt.xlabel("Date"); plt.ylabel("Equity")
        plt.tight_layout()
        plt.savefig("results/outputs/equity_curve.png", dpi=150)

    print("[OK] Saved results in results/outputs")
    print(summary)

if __name__ == "__main__":
    main()
