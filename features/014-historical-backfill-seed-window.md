---
id: 014
name: Historical Backfill (Seed Window)
status: Completed
completed_date: 2026-01-30
---

# 014 - Historical Backfill (Seed Window)

Seed a minimum historical window so that rolling metrics (5-day averages, 14-day ranges) and backtesting can run.

## Description

- Backfill the last N days (recommended: 90) of daily bars for the universe.
- Support incremental catch-up (e.g., new symbols added later).
- Provide a manual command to trigger/extend backfill.

## Impact

- Enables analytics immediately without waiting weeks for data to accumulate.

## Success Criteria

- [x] Backfill completes for at least ASX300 fallback set.
- [x] Rolling metrics can be computed for all symbols with adequate history.
- [x] Backfill can be restarted without corrupting data.

## Implementation Notes

### Location
`jobs/src/asx_jobs/jobs/ingest_prices.py` - `BackfillPricesJob` class

### Supported Periods
| Period | Description |
|--------|-------------|
| `1mo` | 1 month |
| `3mo` | 3 months |
| `6mo` | 6 months |
| `1y` | 1 year |
| `2y` | 2 years (default) |
| `5y` | 5 years |
| `max` | All available history |

### Commands
```bash
asx-jobs backfill              # Default 2-year backfill
asx-jobs backfill --period 1y  # 1-year backfill
asx-jobs backfill --period 5y  # 5-year backfill
```

### Features
- Idempotent upsert (safe to restart)
- Per-symbol progress logging
- Continues on individual symbol failures
- Reports total processed/failed counts
