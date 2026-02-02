---
id: 002
title: price_movement_signals fails due to signal_type enum mismatch
status: Resolved
priority: Medium
component: jobs/signals (price_movement_signals)
date_reported: 2026-02-02
date_resolved: 2026-02-02
---

# 002 - price_movement_signals fails due to signal_type enum mismatch

During the daily orchestrator run, `price_movement_signals` fails inserts with Postgres error `22P02` because `signal_type` values being written (e.g., `volume_spike`, `momentum`) are not valid for the database enum.

## Impact

- Signal generation is partially/non-functional (example run: **6 processed, 47 failed**), so signals are missing from Supabase.
- Any UI/alerting dependent on these signals will be incomplete.

## Steps to Reproduce

1. Run the daily jobs (example): `asx-jobs daily`.
2. Observe `price_movement_signals` output.
3. Confirm repeated errors like:
   - `invalid input value for enum signal_type: "volume_spike"` (Postgres code `22P02`)
   - `invalid input value for enum signal_type: "momentum"` (Postgres code `22P02`)

## Evidence / Logs

- Example (2026-02-02):
  - `[SUCCESS] price_movement_signals: 6 processed, 47 failed (14.1s)`
  - Errors included tickers such as: `ALQ, ALX, ANN, APA, APX, AZJ, BEN, BHP, CAR, CCP`.

## Cause

Schema/code mismatch:
- The jobs runner is attempting to insert new `signal_type` values that are not present in the Postgres enum used by the destination table.

Confirmed enum values (Supabase SQL editor, 2026-02-02):
- `price_movement`
- `volatility_spike`
- `gap_up`
- `gap_down`
- `volume_surge`
- `breakout`
- `breakdown`
- `custom`

Observed job attempts (from logs): `volume_spike`, `momentum`.

## Lessons Learned

- Treat enum changes as coordinated releases: update DB migration and jobs code together.
- Add a startup check in the signals job to validate supported `signal_type` values (fail fast with a clear message).

## Feedback

- Priority set to Medium by request (2026-02-02). Marked as intended-to-fix.

## Resolution

Fixed in `jobs/src/asx_jobs/signals/price_movement.py` by mapping invalid values to valid enum values:

| Invalid Value | Mapped To |
|---------------|-----------|
| `"momentum"` | `"price_movement"` |
| `"volume_spike"` | `"volume_surge"` |
| `"up"` | `"bullish"` |
| `"down"` | `"bearish"` |
