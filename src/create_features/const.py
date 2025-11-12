# constants for create_features module

COLMAP = {
    "symbol": "Ticker",
    "date": "Date",
    "open": "Open",
    "high": "High",
    "low": "Low",
    "close": "Close",
    "volume": "Volume",
}
PARAMS = {
    "short": 12, "mid": 20, "long": 50, "verylong": 200,
    "rsi_len": 14, "stoch_len": 14, "adx_len": 14, "atr_len": 14, "cci_len": 20,
    "bb_len": 20, "macd_fast": 12, "macd_slow": 26, "macd_sig": 9,
    "kama_len": 10, "mfi_len": 14, "roc_len": 12,
}


INDICATORS = [
    ("sma",   {"length": PARAMS["mid"]}),               
    ("sma",   {"length": PARAMS["long"]}),
    ("ema",   {"length": PARAMS["mid"]}),
    ("ema",   {"length": PARAMS["long"]}),
    ("kama",  {"length": PARAMS["kama_len"]}),
    ("wma",   {"length": PARAMS["mid"]}),
    ("hma",   {"length": PARAMS["mid"]}),
    ("rma",   {"length": PARAMS["mid"]}),

    ("atr",   {"length": PARAMS["atr_len"]}),
    ("bbands",{"length": PARAMS["bb_len"]}), 

    ("rsi",   {"length": PARAMS["rsi_len"]}),
    ("stoch", {"k": PARAMS["stoch_len"], "d": 3, "smooth_k": 3}),
    ("macd",  {"fast": PARAMS["macd_fast"], "slow": PARAMS["macd_slow"], "signal": PARAMS["macd_sig"]}),
    ("ppo",   {"fast": PARAMS["macd_fast"], "slow": PARAMS["macd_slow"], "signal": PARAMS["macd_sig"]}),
    ("roc",   {"length": PARAMS["roc_len"]}),
    ("mom",   {"length": PARAMS["roc_len"]}),
    ("tsi",   {"long": 25, "short": 13}),
    ("wr",    {"lbp": 14}),
    ("ao",    {}),                                           # Awesome Oscillator
    ("pgo",   {}),                                           # Pretty Good Oscillator（论文示例之一）
    ("qqe",   {"length": 14}),

    ("mfi",   {"length": PARAMS["mfi_len"]}),
    ("obv",   {}),
    ("pvo",   {"fast": 12, "slow": 26, "signal": 9}),        # 论文示例之一（PVO）
    ("ad",    {}),                                           # Accumulation/Distribution
    ("adosc", {"fast": 3, "slow": 10}),
    ("cmf",   {"length": 20}),
    ("vwap",  {}),
    
    ("adx",   {"length": PARAMS["adx_len"]}),
    ("aroon", {"length": 25}),
    ("dpo",   {"length": 20}),
    ("vortex",{"length": 14}),
    ("supertrend", {"length": 10, "multiplier": 3.0}),

    # 价格形态/摆动
    ("cci",   {"length": PARAMS["cci_len"]}),
    ("donchian", {"lower_length": 20, "upper_length": 20}),
    ("keltner",  {"length": 20}),
    ("psar",  {"step": 0.02, "max_step": 0.2}),
    ("uo",    {"fast": 7, "medium": 14, "slow": 28}), 

    ("rvi",   {"length": 10}),
    ("pvi",   {}),                                           # Positive Volume Index
    ("nvi",   {}),                                           # Negative Volume Index
    ("vwma",  {"length": 20}),
    ("zscore",{"length": 20}),
    ("trix",  {"length": 18}),
    ("eri",   {}),                                           # Elder Ray Index
    ("tsi",   {"long": 25, "short": 13}),                    # 与上重复可删；此处占位
    ("kvo",   {"fast": 34, "slow": 55}), 
                      
    ("qstick",{"length": 14}),
    ("pvol",  {"length": 20}),                               # pandas_ta的量能动量（若无则跳过）
    ("rvgi",  {"length": 14}),
    ("cg",    {"length": 10}),                               # Center of Gravity
    ("mad",   {"length": 20}),
    ("median",{"length": 20}),
    ("stdev", {"length": 20}),
    ("variance", {"length": 20}),
    ("entropy", {"length": 5}),                              # 信息熵（pandas_ta 有 ta.entropy）
    ("tsignals", {"length": 10}),                            # 趋势信号（若不可用自动跳过）
    ("inertia", {"length": 20}),                 
]