def decide(report, strategy, risk_eval, sim_reward, real_reward):
    # 双重奖励（玩具版）：实盘权重大于模拟
    w_sim, w_real = 0.4, 0.6
    score = w_sim*sim_reward + w_real*real_reward - 0.5*risk_eval["risk_score"]
    if score > 0.05:
        return {"action":"BUY", "allocation": min(0.8, max(0.2, score)), "score": score}
    elif score < -0.05:
        return {"action":"SELL", "allocation": 0.0, "score": score}
    else:
        return {"action":"HOLD", "allocation": 0.0, "score": score}
