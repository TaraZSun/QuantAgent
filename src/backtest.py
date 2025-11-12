# src/backtest.py
import pandas as pd
import numpy as np

def backtest_long_only(close: pd.Series, signal: pd.Series, cash: float = 100000.0):
    close = close.dropna().astype(float)
    signal = signal.reindex(close.index).fillna(0).astype(float)

    ret = close.pct_change().fillna(0.0)
    strat_ret = ret * signal.shift(1).fillna(0)  # 用前一日信号进场
    equity = (1 + strat_ret).cumprod()
    equity = equity * (cash / equity.iloc[0])

    ann = 252
    arr = (equity.iloc[-1] / equity.iloc[0]) ** (ann / len(equity)) - 1
    vol = strat_ret.std() * (ann ** 0.5)
    sharpe = arr / (vol + 1e-12)
    roll_max = equity.cummax()
    mdd = ((equity - roll_max) / roll_max).min()

    return {
        "equity": equity,
        "daily_returns": strat_ret,
        "ARR": float(arr),
        "Sharpe": float(sharpe),
        "MDD": float(mdd),
        "Volatility": float(vol),
    }
