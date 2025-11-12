from src.indicators import sma, rsi

def propose_strategy(df, sma_fast=20, sma_slow=50, rsi_th=55):
    # 固定一个 v1 规则策略
    return {
        "type": "strategy",
        "detail": {
            "name": "SMA20_SMA50_RSI55",
            "logic": "long if SMA20>SMA50 and RSI>55 else flat",
            "params": {"sma_fast": sma_fast, "sma_slow": sma_slow, "rsi": rsi_th}
        }
    }
