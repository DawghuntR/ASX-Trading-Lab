---
id: 016
name: Signal Engine - Price Movement Tracker
status: Completed
completed_date: 2026-01-30
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

- Provides the first actionable "scanner-like" output.

## Success Criteria

- [x] Signals are generated daily and stored in Supabase.
- [x] Each signal includes symbol, timestamp, type, metrics, and trigger reason.
- [x] Dashboard can list "top movers / unusual activity" for the day.

## Implementation Notes

### Location
`jobs/src/asx_jobs/signals/price_movement.py`

### Signal Types Generated

| Signal Type | Trigger | Default Threshold |
|-------------|---------|-------------------|
| `price_movement` | Daily % change | ±5% |
| `momentum` | 5-day % change | ±10% |
| `volume_spike` | Volume vs 20-day avg | 2x |

### Configuration (`PriceMovementConfig`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `daily_change_threshold` | 5.0% | Min % change for price movement signal |
| `five_day_change_threshold` | 10.0% | Min % change for momentum signal |
| `volume_spike_multiplier` | 2.0x | Volume ratio threshold |
| `volume_baseline_days` | 20 | Days for volume average baseline |
| `min_price` | $0.01 | Minimum price to generate signals |

### Signal Strength Levels
- **weak**: Just above threshold
- **medium**: Between threshold and high threshold
- **strong**: Above high threshold (3x base threshold)

### Commands
```bash
asx-jobs daily    # Runs price ingestion + signal generation
asx-jobs signals  # Runs signal generation only
```

### Signal Record Structure
```json
{
  "instrument_id": 123,
  "signal_date": "2026-01-30",
  "signal_type": "price_movement",
  "direction": "up",
  "strength": "strong",
  "trigger_price": 45.67,
  "trigger_reason": "Daily change +8.5% exceeds 5% threshold",
  "metrics": {
    "daily_change_pct": 8.5,
    "close": 45.67,
    "volume": 1234567
  }
}
```
