---
id: 014
name: Historical Backfill (Seed Window)
status: Planned
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

- Backfill completes for at least ASX300 fallback set.
- Rolling metrics can be computed for all symbols with adequate history.
- Backfill can be restarted without corrupting data.
