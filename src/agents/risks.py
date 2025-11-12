def assess_risk(metrics):
    # 用最大回撤粗略映射到 risk_score
    mdd = abs(metrics.get("MDD", 0))
    risk_score = min(1.0, max(0.0, mdd / 0.30))  # |MDD|/0.30 截断
    advice = f"回撤 {mdd:.2%}，风险评分 {risk_score:.2f}。建议控制仓位上限 50%，设 5%-8% 止损。"
    return {"type":"risk", "advice": advice, "risk_score": risk_score}
