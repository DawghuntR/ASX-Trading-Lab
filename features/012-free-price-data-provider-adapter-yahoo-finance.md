---
id: 012
name: Free Price Data Provider Adapter (Yahoo Finance)
status: Completed
completed_date: 2026-01-30
---

# 012 - Free Price Data Provider Adapter (Yahoo Finance)

Implement a free, no-key price data adapter (best-effort) to fetch daily bars and a "latest" snapshot suitable for midday scans.

## Description

- Implement provider client to retrieve:
  - daily OHLCV bars (historical)
  - latest quote (for "today" snapshot)
- Handle rate limiting and batching across many symbols.
- Implement retries and caching to reduce load.
- Document provider limitations (no SLA) and the fallback plan (Feature 014/015 scraping).

## Impact

- Enables zero-cost ingestion across many instruments.
- Provides the dataset required for signals and backtesting.

## Success Criteria

- [x] Can fetch daily bars for a test symbol and store in DB via jobs runner.
- [x] Can fetch recent data (within last week) reliably enough for daily runs.
- [x] Degrades gracefully (logs failures, continues with partial success where appropriate).

## Implementation Notes

### Location
`jobs/src/asx_jobs/providers/yahoo.py`

### Features
- Uses `yfinance` library for Yahoo Finance API access
- Rate limiting: 0.5 second delay between requests
- Retry with exponential backoff (3 attempts, 2-10 second delays)
- Batch processing with configurable batch size
- Returns standardized `PriceBar` dataclass

### API Methods
| Method | Description |
|--------|-------------|
| `get_daily_bars(symbol, period)` | Fetch historical OHLCV data |
| `get_latest_quote(symbol)` | Fetch current/latest price |
| `get_info(symbol)` | Fetch company metadata |

### Rate Limiting Strategy
- 0.5 second delay between individual requests
- Batch processing: 50 symbols per batch with 5 second inter-batch delay
- Retry on failure: exponential backoff (2s, 4s, 8s)

### Provider Limitations
- No SLA (free tier, best-effort)
- May experience rate limiting during market hours
- Data may be delayed 15-20 minutes
- Weekend/holiday data may be stale

### Fallback Plan
If Yahoo Finance becomes unreliable, Feature 031 (Python web scraping) provides an alternative data source.
