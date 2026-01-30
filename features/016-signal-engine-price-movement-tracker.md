---
id: 016
name: Signal Engine - Price Movement Tracker
status: Planned
---

# 016 - Signal Engine: Price Movement Tracker

Compute daily momentum/abnormal movement signals and persist them for display in the dashboard.

## Description

On the daily run, compute per symbol:

- % change today (relative to prior close)
- % change vs 5-day average (define exact formula in implementation)
- unusual volume (define baseline window + threshold)

Persist signals with a clear reason string and supporting metrics.

## Impact

- Provides the first actionable “scanner-like” output.

## Success Criteria

- Signals are generated daily and stored in Supabase.
- Each signal includes symbol, timestamp, type, metrics, and trigger reason.
- Dashboard can list “top movers / unusual activity” for the day.
