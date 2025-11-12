# src/risk_alert.py
import numpy as np
import pandas as pd

def check_risk_alert(
    equity: pd.Series,
    daily_returns: pd.Series,
    mdd_thresh: float = 0.20,      # 最大回撤阈值（20%）
    vol_thresh: float = 0.30,      # 年化波动阈值（30%）
    window: int = 60               # 近 N 日评估窗口
):
    alert_reasons = []

    # 1) 近 N 日滚动最大回撤
    eq = equity.dropna()
    if len(eq) >= window:
        recent = eq.iloc[-window:]
        roll_max = recent.cummax()
        recent_mdd = float(((recent - roll_max) / roll_max).min())  # 负数
        if abs(recent_mdd) >= mdd_thresh:
            alert_reasons.append(f"近期{window}日最大回撤 {abs(recent_mdd):.2%} ≥ {mdd_thresh:.0%}")

    # 2) 年化波动率（近 N 日）
    dr = daily_returns.dropna()
    if len(dr) >= window:
        recent_vol = float(dr.iloc[-window:].std() * (252 ** 0.5))
        if recent_vol >= vol_thresh:
            alert_reasons.append(f"近期{window}日年化波动 {recent_vol:.2%} ≥ {vol_thresh:.0%}")

    fired = len(alert_reasons) > 0
    return {
        "fired": fired,
        "reasons": alert_reasons,
        "params": {"mdd_thresh": mdd_thresh, "vol_thresh": vol_thresh, "window": window}
    }
