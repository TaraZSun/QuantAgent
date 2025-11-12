def analyze_market(df):
    # 简单模板：用最近一段的涨跌 + 波动 生成一句中文摘要
    recent = df["close"].pct_change().tail(20).dropna()
    drift = recent.mean() * 252
    vol = recent.std() * (252 ** 0.5)
    if drift > 0.05:
        tone = "偏多"
    elif drift < -0.05:
        tone = "偏空"
    else:
        tone = "中性"
    return {
        "type": "market_report",
        "summary": f"近20日年化漂移约 {drift:.2%}，年化波动约 {vol:.2%}，市场情绪{tone}，建议小仓位观察。"
    }
