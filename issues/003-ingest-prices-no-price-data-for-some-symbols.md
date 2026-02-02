---
id: 003
title: ingest_prices reports no price data for some symbols
status: Open
priority: Low
component: jobs/ingest_prices
date_reported: 2026-02-02
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

TBD.

Likely possibilities:
- Delisted/renamed tickers still present in the symbols universe.
- Upstream provider does not cover the symbol.
- Market segment / instrument type mismatch (non-equity tickers, etc.).

## Lessons Learned

- Maintain an “active/universe” flag and/or symbol mapping to reduce expected misses.
- Track “no price data” as a separate category from true operational failures.
