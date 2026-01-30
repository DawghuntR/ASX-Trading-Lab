---
id: 017
name: Signal Engine - Volatility Spike Watcher
status: Completed
completed_date: 2026-01-30
---

# 017 - Signal Engine: Volatility Spike Watcher

Detect and persist daily volatility spike signals based on recent average ranges.

## Description

- Compute 14-day average daily range (define range measure: high-low, or ATR-like approximation on daily bars).
- Compare today's range (or most recent bar) to the baseline.
- Trigger when today exceeds a multiplier (e.g., > 2×).

## Impact

- Highlights abnormal activity likely tied to catalysts.

## Success Criteria

- [x] Volatility signals are generated daily and stored in Supabase.
- [x] Parameters (window, multiplier) are configurable.
- [x] UI can filter and display volatility spike events.

## Implementation Notes

### Location
`jobs/src/asx_jobs/signals/volatility.py`

### Signal Type
- `volatility_spike` - Triggered when daily True Range exceeds ATR threshold

### True Range Calculation
```
True Range = max(
    high - low,
    abs(high - previous_close),
    abs(low - previous_close)
)
```

### Configuration (`VolatilityConfig`)

| Parameter | Default | Description |
|-----------|---------|-------------|
| `atr_window` | 14 | Days for ATR calculation |
| `spike_multiplier` | 2.0x | Threshold for weak/medium signal |
| `strong_spike_multiplier` | 3.0x | Threshold for strong signal |
| `min_price` | $0.01 | Minimum price to generate signals |
| `min_atr` | 0.001 | Minimum ATR to avoid div-by-zero |

### Signal Strength Levels
- **weak**: Range ratio 2.0x - 2.5x ATR
- **medium**: Range ratio 2.5x - 3.0x ATR
- **strong**: Range ratio > 3.0x ATR

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
  "signal_type": "volatility_spike",
  "direction": "neutral",
  "strength": "strong",
  "trigger_price": 45.67,
  "trigger_reason": "Daily range 3.2x above 14-day ATR",
  "metrics": {
    "true_range": 2.34,
    "atr": 0.73,
    "range_ratio": 3.2,
    "atr_window": 14,
    "high": 47.50,
    "low": 45.16,
    "close": 45.67
  }
}
```
