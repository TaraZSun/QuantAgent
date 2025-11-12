#!/usr/bin/env python3
import argparse, os, json
import pandas as pd
from subprocess import run, CalledProcessError

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tickers", required=True, help="e.g., AAPL,MSFT,NVDA")
    ap.add_argument("--start", required=True)
    ap.add_argument("--end", required=True)
    ap.add_argument("--cash", type=float, default=100000)
    args = ap.parse_args()

    os.makedirs("results/reports", exist_ok=True)
    rows = []
    for t in [x.strip() for x in args.tickers.split(",") if x.strip()]:
        raw = f"data/raw/{t}_{args.start}_{args.end}_std.csv"
        sig = f"data/processed/{t}_{args.start}_{args.end}_std_signals.csv"

        # 如果还没做信号，就先做一次
        if not os.path.exists(sig):
            run(["python", "src/make_signals.py", "--infile", raw], check=True)

        # 跑会议流（会写 results/outputs 下，但我们读 summary.json）
        run(["python", "-m", "src.pipeline", "--signals", sig, "--cash", str(args.cash), "--plot", "0"], check=True)

        # 读取 summary 并记录
        with open("results/outputs/summary.json", "r", encoding="utf-8") as f:
            s = json.load(f)
        rows.append({
            "ticker": t,
            "ARR": s["sim_metrics"]["ARR"],
            "Sharpe": s["sim_metrics"]["Sharpe"],
            "MDD": s["sim_metrics"]["MDD"],
            "Volatility": s["sim_metrics"]["Volatility"],
            "decision_action": s["decision"]["action"],
            "decision_score": s["decision"]["score"],
        })

    df = pd.DataFrame(rows)
    out = f"results/reports/summary_{args.start}_{args.end}.csv"
    df.to_csv(out, index=False)
    print(f"[saved] {out}\n")
    print(df)

if __name__ == "__main__":
    main()
