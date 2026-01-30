---
id: 032
name: Symbol Normalization & Provider Mapping
status: Planned
---

# 032 - Symbol Normalization & Provider Mapping

Standardize how ASX symbols are represented across the database, providers, and UI, including mapping to provider-specific tickers.

## Description

- Define a canonical symbol format in the database (e.g., `BHP` + exchange `ASX`).
- Maintain mappings for provider tickers (e.g., Yahoo may require suffixes).
- Handle edge cases:
  - delisted symbols
  - corporate actions (renames)
  - non-equities if they appear in the universe source

## Impact

- Prevents data fragmentation and mismatches across ingestion and analytics.

## Success Criteria

- Every instrument has a stable internal id.
- Provider queries can be generated deterministically from mappings.
- UI uses canonical symbols while providers use mapped tickers.
