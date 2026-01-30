---
id: 013
name: Daily Price Ingestion (OHLCV + Midday Snapshot)
status: Planned
---

# 013 - Daily Price Ingestion (OHLCV + Midday Snapshot)

Ingest daily OHLCV data (and capture a midday “latest” snapshot) for the configured ASX universe into Supabase.

## Description

- On the daily run (~12:00 Sydney):
  - fetch latest quote/snapshot per symbol
  - ensure daily OHLCV for recent days is present
- Use upsert patterns to avoid duplication.
- Store ingestion job metadata (run id, duration, failures).

## Impact

- Establishes a dependable dataset for scanning, analytics, and UI.

## Success Criteria

- Whole-of-ASX (or ASX300 fallback) daily refresh completes within an acceptable window for home-lab resources.
- Data is queryable in Supabase for:
  - latest snapshot per symbol
  - daily bars for the last N days
- Failures are recorded with enough detail to retry.
