# QuantAgents 复现计划（免费方案）

本试验目标：用免费资源复现论文提出的“多智能体 + 模拟交易 + 双重奖励”的核心思想，先做能跑通的 MVP，再逐步增强。[思维导图](docs/quantagents_mindmap_compact.svg)


Paper 目标：构建一个融入“模拟交易”的多智能体金融系统（QuantAgents），让智能体不仅依赖事后反思，还能进行面向未来的长期预测；
通过模拟交易在零真实风险下评估策略，并结合真实市场收益与模拟预测准确度的“双重奖励”来协同四个角色（交易、风控、新闻与经理）做出更前瞻的投资决策。


🔭 路线图（分阶段）

## Phase 0 — 环境与数据通路

 创建虚拟环境，安装依赖

 用yfinance拉取10个NASDAQ中公司的历史数据从2010-2023，保存为标准化的CSV，并将数据保存为parquet的形式，位置后的百万数据做好扩展的准备，并用于接下来的处理

 基于每日 OHLCV/AdjClose 为每只股票批量生成 10 个经典技术指标（SMA20/50、EMA20、RSI14、MACD、ATR14、BBands20、ADX14、MFI14、OBV），并统一 滞后 1 日 防前视，结果保存到 data/clean/features_10/（Parquet）

## Phase 1 — 最小可运行 Demo

指标计算：SMA/EMA/RSI

策略 v1：SMA20>SMA50 & RSI>55 做多，否则空仓

 回测引擎 v1：日频、长多/空仓（无手续费）

 输出：权益曲线、ARR、Sharpe、MDD

 文档：如何复现实验（命令、默认参数）

## Phase 2 — 多智能体骨架

 4个“角色”类：Market、Strategy、Risk、Manager

 “会议流”：市场分析 → 策略提案+回测 → 风险评估 → 经理决策

 记忆模块 v1：JSON 持久化（reports/strategies/risks）

 双重奖励 v1：sim_reward=回测ARR；real_reward=近60日B&H 年化；score = 0.4*sim + 0.6*real - 0.5*risk_score

## Phase 3 — 评估与消融

 多标的：AAPL / MSFT / NVDA（单资产独立评估）

 统一指标对比表：ARR、Sharpe、MDD、Vol

 消融：去掉会议/去掉模拟/去掉风险 ⇒ 对比性能变化

 固定随机种子、导出 results/summary.csv

## Phase 4 — 进阶

 多资产组合（均权 or 风险平价）

 策略池（动量、反转、波动率分层），会议选择最优

 风险预警阈值触发（VaR/Beta/波动率）

 本地 LLM（Ollama）+ JSON 工具调用（仍然免费）