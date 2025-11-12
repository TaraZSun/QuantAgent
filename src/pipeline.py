#!/usr/bin/env python3
import argparse, os, json
import pandas as pd
from src.indicators import sma, rsi
from src.backtest import backtest_long_only
from src.memory import JsonMemory
from src.agents.market import analyze_market
from src.agents.strategy import propose_strategy
from src.agents.risks import assess_risk
from src.agents.manager import decide
from src.risk_alert import check_risk_alert


def build_signal(df, params):
    s20 = sma(df["close"], params["sma_fast"])
    s50 = sma(df["close"], params["sma_slow"])
    r = rsi(df["close"], 14)
    return ((s20 > s50) & (r > params["rsi"])).astype(int)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--signals", required=True, help="data/processed/..._signals.csv")
    ap.add_argument("--cash", type=float, default=100000)
    ap.add_argument("--plot", type=int, default=1)
    args = ap.parse_args()

    os.makedirs("results/outputs", exist_ok=True)
    memory = JsonMemory("results/outputs/memory.json")

    # 读取带信号的数据（含 close/signal）
    df = pd.read_csv(args.signals, parse_dates=["date"]).set_index("date")

    # Meeting 1: Market Analysis
    report = analyze_market(df)
    memory.append("reports", {"report": report})
    print("\n[Market Analysis]\n", report["summary"])

    # Meeting 2: Strategy Development (+ simulated trading)
    strat = propose_strategy(df)
    params = strat["detail"]["params"]
    signal = df["signal"] if "signal" in df.columns else build_signal(df, params)
    sim_res = backtest_long_only(df["close"], signal, cash=args.cash)
    sim_reward = sim_res["ARR"]  # 玩具：用 ARR 代表模拟奖励
    memory.append("strategies", {"strategy": strat, "sim_metrics": {k:v for k,v in sim_res.items() if k not in ("equity","daily_returns")}})
    print("\n[Strategy Development]\n", strat)

    # Meeting 3: Risk Assessment
    risk_eval = assess_risk(sim_res)
    memory.append("risks", risk_eval)
    print("\n[Risk Assessment]\n", risk_eval["advice"], f"(risk_score={risk_eval['risk_score']:.2f})")

    # Risk Alert Trigger（基于近60日 MDD/波动率）
    alert = check_risk_alert(sim_res["equity"], sim_res["daily_returns"],
                             mdd_thresh=0.20, vol_thresh=0.30, window=60)
    if alert["fired"]:
        print("\n[Risk Alert] 触发预警：")
        for r in alert["reasons"]:
            print(" -", r)
    else:
        print("\n[Risk Alert] 未触发。")


    # Real reward（玩具）：近 60 日买入持有的年化收益
    bh = (1 + df["close"].pct_change().fillna(0)).cumprod()
    window = 60
    if len(bh) > window:
        recent = bh.iloc[-window:]
        growth = recent.iloc[-1] / recent.iloc[0]
        real_reward = growth ** (252/window) - 1
    else:
        real_reward = 0.0

    decision = decide(report, strat, risk_eval, sim_reward=sim_reward, real_reward=real_reward)
    
    # 如果触发风险预警，强制降档：BUY 最多 20% 仓位；若风险评分也很高则直接 SELL
    if alert["fired"]:
        # 简单策略：若 risk_score >= 0.8 则清仓；否则 BUY 限制为 0.2
        if risk_eval["risk_score"] >= 0.8:
            decision["action"] = "SELL"
            decision["allocation"] = 0.0
            decision["reason"] = "Risk alert + high risk score (>=0.8)"
        elif decision["action"] == "BUY" and decision.get("allocation", 0) > 0.2:
            decision["allocation"] = 0.2
            decision["reason"] = "Risk alert cap allocation at 20%"

    print("\n[Manager Decision]\n", decision)

    # —— 保存输出文件 ——
    os.makedirs("results/outputs", exist_ok=True)

    # 1) 权益曲线（CSV）
    sim_res["equity"].to_csv("results/outputs/equity_curve.csv")

    # 2) 决策（decision.json）
    #    将 numpy.float64 转成 float，避免 JSON 里出现不可序列化类型
    decision_json = {k: (float(v) if hasattr(v, "__float__") else v) for k, v in decision.items()}
    with open("results/outputs/decision.json", "w", encoding="utf-8") as f:
        json.dump(decision_json, f, ensure_ascii=False, indent=2)

    # 3) summary.json（含主要指标 + 决策 + 风险预警信息）
    summary = {
        "sim_metrics": {
            "ARR": float(sim_res["ARR"]),
            "Sharpe": float(sim_res["Sharpe"]),
            "MDD": float(sim_res["MDD"]),
            "Volatility": float(sim_res["Volatility"]),
        },
        "decision": decision_json,
        # 如果你已接入 risk_alert 模块，这里写 alert；如果还没接，就先放 None
        "risk_alert": alert if "alert" in locals() else None
    }
    with open("results/outputs/summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("\n[Done] Saved results in results/outputs")


    # 保存主要输出
    sim_res["equity"].to_csv("results/outputs/equity_curve.csv")
    summary = {
        "sim_metrics": {k: float(v) for k,v in sim_res.items() if k not in ("equity","daily_returns")},
        "decision": decision
    }
    with open("results/outputs/summary.json","w",encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    with open("results/outputs/decision.json","w",encoding="utf-8") as f:
        json.dump(decision, f, ensure_ascii=False, indent=2)

    print("\n[Done] Saved results in results/outputs")

if __name__ == "__main__":
    main()
