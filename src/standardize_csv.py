#!/usr/bin/env python3
import argparse, os, re
import pandas as pd

def find_data_start(df):
    """找到第一行真正数据（首列是 YYYY-MM-DD 的地方）"""
    date_pat = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    for i, v in enumerate(df.iloc[:, 0].astype(str)):
        if date_pat.match(v.strip()):
            return i
    raise SystemExit("未找到以 YYYY-MM-DD 开头的数据行，请检查文件。")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--infile", required=True, help="原始 CSV 路径")
    ap.add_argument("--outfile", default=None, help="输出标准化 CSV 路径（默认 data/raw/<name>_std.csv）")
    args = ap.parse_args()

    # 不信任原表头：用 header=None 读入
    raw = pd.read_csv(args.infile, header=None)
    start_idx = find_data_start(raw)

    # 从数据行开始取，并设置标准列名
    df = raw.iloc[start_idx:].copy()
    df.columns = ["date", "open", "high", "low", "close", "volume"]

    # 类型与清洗
    df["date"] = pd.to_datetime(df["date"])
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["open","high","low","close","volume"])
    df = df.sort_values("date").reset_index(drop=True)

    # 输出
    if args.outfile is None:
        os.makedirs("data/raw", exist_ok=True)
        base = os.path.basename(args.infile).replace(".csv", "")
        args.outfile = os.path.join("data/raw", f"{base}_std.csv")

    df.to_csv(args.outfile, index=False)
    print(f"[saved] {args.outfile}  rows={len(df)}")
    print(df.head(3))

if __name__ == "__main__":
    main()
