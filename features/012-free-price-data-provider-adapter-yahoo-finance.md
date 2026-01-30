---
id: 012
name: Free Price Data Provider Adapter (Yahoo Finance)
status: Planned
---

# 012 - Free Price Data Provider Adapter (Yahoo Finance)

Implement a free, no-key price data adapter (best-effort) to fetch daily bars and a “latest” snapshot suitable for midday scans.

## Description

- Implement provider client to retrieve:
  - daily OHLCV bars (historical)
  - latest quote (for “today” snapshot)
- Handle rate limiting and batching across many symbols.
- Implement retries and caching to reduce load.
- Document provider limitations (no SLA) and the fallback plan (Feature 014/015 scraping).

## Impact

- Enables zero-cost ingestion across many instruments.
- Provides the dataset required for signals and backtesting.

## Success Criteria

- Can fetch daily bars for a test symbol and store in DB via jobs runner.
- Can fetch recent data (within last week) reliably enough for daily runs.
- Degrades gracefully (logs failures, continues with partial success where appropriate).
