---
id: 017
name: Signal Engine - Volatility Spike Watcher
status: Planned
---

# 017 - Signal Engine: Volatility Spike Watcher

Detect and persist daily volatility spike signals based on recent average ranges.

## Description

- Compute 14-day average daily range (define range measure: high-low, or ATR-like approximation on daily bars).
- Compare today’s range (or most recent bar) to the baseline.
- Trigger when today exceeds a multiplier (e.g., > 2×).

## Impact

- Highlights abnormal activity likely tied to catalysts.

## Success Criteria

- Volatility signals are generated daily and stored in Supabase.
- Parameters (window, multiplier) are configurable.
- UI can filter and display volatility spike events.
