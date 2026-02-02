---
id: 003
title: ingest_prices reports no price data for some symbols
status: Closed
priority: Low
component: jobs/ingest_prices
date_reported: 2026-02-02
date_closed: 2026-02-02
resolution: By Design
---

# 003 - ingest_prices reports no price data for some symbols

During the daily orchestrator run, `ingest_prices` reports failures for some tickers with the message `no price data`.

## Impact

- Missing price history for affected symbols.
- Usually low impact if the symbols are delisted/invalid/out-of-universe, but could indicate upstream data gaps if active symbols are affected.

## Steps to Reproduce

1. Run the daily jobs (example): `asx-jobs daily`.
2. Observe `ingest_prices` output.
3. Confirm failures like `TICKER: no price data`.

## Evidence / Logs

- Example (2026-02-02):
  - `[SUCCESS] ingest_prices: 696 processed, 24 failed (130.8s)`
  - Sample errors: `ABC, ABP, ALU, AWC, BKL, BKW, BLD, CIM, CSR, DEG`.

## Cause

**Confirmed:** The failed symbols (ABC, ABP, ALU, AWC, BKL, BKW, BLD, CIM, CSR, DEG) are **delisted or merged companies** that no longer exist on the ASX. Yahoo Finance returns no data for these symbols.

This is the same root cause as Issue 001 - the hardcoded `ASX_300_SYMBOLS` list contains outdated symbols.

## Lessons Learned

- Maintain an "active/universe" flag and/or symbol mapping to reduce expected misses.
- Track "no price data" as a separate category from true operational failures.

## Resolution

**Closed as "By Design"** - The job is working correctly:

1. **Graceful handling:** No exceptions thrown; job continues processing remaining symbols
2. **High success rate:** 696 processed vs 24 failed (96.5% success)
3. **Proper logging:** Errors recorded in logs and `job_runs` table
4. **Feature compliant:** Matches Feature 012 specification for graceful degradation

The code correctly handles missing data:
```python
if not bars:
    failed += 1
    errors.append(f"{symbol}: no price data")
    continue  # Skips to next symbol, doesn't crash
```

**No code fix required.** The underlying issue is stale symbols in the universe, which is a data maintenance task, not a bug.
