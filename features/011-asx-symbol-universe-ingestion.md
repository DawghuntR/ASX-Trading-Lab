---
id: 011
name: ASX Symbol Universe Ingestion
status: Planned
---

# 011 - ASX Symbol Universe Ingestion

Ingest the ASX symbol universe into Supabase, targeting whole-of-ASX with a defined fallback order.

## Description

- Primary: ingest ASX “Listed Companies” CSV into an `instruments` dataset.
- Normalize symbols for downstream providers (e.g., mapping to provider tickers if needed).
- Fallback order if whole-of-ASX becomes impractical on free sources:
  - **ASX300 → ASX200**

## Impact

- Enables scanning beyond a manual watchlist.
- Allows consistent symbol coverage across ingestion and analytics.

## Success Criteria

- Instruments table is populated with whole-of-ASX symbols (or fallback set).
- Symbol normalization rules are documented.
- Universe can be refreshed without duplicating rows.
