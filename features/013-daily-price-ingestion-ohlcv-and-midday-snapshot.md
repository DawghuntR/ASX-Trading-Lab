---
id: 013
name: Daily Price Ingestion (OHLCV + Midday Snapshot)
status: Completed
completed_date: 2026-01-30
---

# 013 - Daily Price Ingestion (OHLCV + Midday Snapshot)

Ingest daily OHLCV data (and capture a midday "latest" snapshot) for the configured ASX universe into Supabase.

## Description

- On the daily run (~12:00 Sydney):
  - fetch latest quote/snapshot per symbol
  - ensure daily OHLCV for recent days is present
- Use upsert patterns to avoid duplication.
- Store ingestion job metadata (run id, duration, failures).

## Impact

- Establishes a dependable dataset for scanning, analytics, and UI.

## Success Criteria

- [x] Whole-of-ASX (or ASX300 fallback) daily refresh completes within an acceptable window for home-lab resources.
- [x] Data is queryable in Supabase for:
  - [x] latest snapshot per symbol
  - [x] daily bars for the last N days
- [x] Failures are recorded with enough detail to retry.

## Implementation Notes

### Location
`jobs/src/asx_jobs/jobs/ingest_prices.py`

### Features
- Batch processing (10 symbols per batch) to optimize API calls
- 30-day lookback window for recent data
- Bulk upsert for efficient database writes
- Detailed logging of processed/failed counts

### Commands
```bash
asx-jobs daily    # Run daily ingestion (symbols + prices)
```

### Data Flow
1. Fetch all active instruments from database
2. Process in batches using Yahoo Finance bulk download
3. Upsert prices with conflict resolution on (instrument_id, trade_date)
