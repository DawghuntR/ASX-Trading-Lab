---
id: 011
name: ASX Symbol Universe Ingestion
status: Completed
completed_date: 2026-01-30
---

# 011 - ASX Symbol Universe Ingestion

Ingest the ASX symbol universe into Supabase, targeting whole-of-ASX with a defined fallback order.

## Description

- Primary: ingest ASX "Listed Companies" CSV into an `instruments` dataset.
- Normalize symbols for downstream providers (e.g., mapping to provider tickers if needed).
- Fallback order if whole-of-ASX becomes impractical on free sources:
  - **ASX300 → ASX200**

## Impact

- Enables scanning beyond a manual watchlist.
- Allows consistent symbol coverage across ingestion and analytics.

## Success Criteria

- [x] Instruments table is populated with whole-of-ASX symbols (or fallback set).
- [x] Symbol normalization rules are documented.
- [x] Universe can be refreshed without duplicating rows.

## Implementation Notes

### Location
`jobs/src/asx_jobs/jobs/ingest_symbols.py`

### Features
- ASX 300 symbol list hardcoded as initial universe
- Symbol normalization: `BHP` → `BHP.AX` for Yahoo Finance
- Idempotent upsert via `upsert_instruments()` database function
- Optional metadata fetch from Yahoo Finance (company name, sector, market cap)
- Rate limiting to avoid API throttling

### Commands
```bash
asx-jobs symbols              # Ingest symbols with metadata
asx-jobs symbols --no-metadata  # Quick ingest without Yahoo API calls
```

### Symbol Normalization Rules
| ASX Symbol | Yahoo Finance Ticker |
|------------|---------------------|
| BHP        | BHP.AX              |
| CBA        | CBA.AX              |
| CSL        | CSL.AX              |

All ASX symbols are suffixed with `.AX` for Yahoo Finance API compatibility.
