## Unstructured Text Data (Alpaca News API)

This module collects **company-related news** from the **Alpaca News API** and stores it
in a structured format for downstream NLP and agent-based research.

> All commands are intended to be run from the project root with the virtual
> environment activated and Alpaca API credentials configured in your environment
> (or `.env`).

---

### 1. Fetch company news from Alpaca

Run the news ingestion script:

```bash
python -m src.process_data.unstructure_data.fetch_alpaca_news
```
This will:
Read the target tickers (e.g. NASDAQ-100 or a custom universe)
Query the Alpaca News API for each ticker over the configured date range
Normalize the raw JSON payloads into a consistent schema
Save the results to disk (e.g. as JSON/Parquet) for later processing

## 2. Pydantic models for unstructured (text) data
The file src/process_data/unstructure_data/models.py
defines the Pydantic models used to represent unstructured textual data from Alpaca, such as:
EntityNewsRaw — raw per-article/per-ticker news records
Other helper models for validation and schema consistency

These models enforce types (e.g. ticker, timestamps, URLs) and ensure that all ingested
news items conform to a well-defined structure before they are used in feature
engineering or agent simulations.