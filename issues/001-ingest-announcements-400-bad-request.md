---
id: 001
title: ingest_announcements fails with 400 Bad Request for many tickers
status: Resolved
priority: Medium
component: jobs/ingest_announcements
date_reported: 2026-02-02
date_resolved: 2026-02-02
---

# 001 - ingest_announcements fails with 400 Bad Request for many tickers

During the daily orchestrator run, `ingest_announcements` reports a very high failure rate with HTTP 400 responses from the ASX Markit Digital announcements endpoint.

## Impact

- Announcements ingestion becomes largely ineffective (example run: **1 processed, 24 failed**), resulting in missing announcements data in Supabase.
- Downstream features that rely on announcements (dashboards, alerts, analytics) may be incomplete or misleading.

## Steps to Reproduce

1. Run the daily jobs (example): `asx-jobs daily`.
2. Observe `ingest_announcements` output.
3. Confirm repeated failures like:
   - `fetch failed - 400 Client Error: Bad Request for url: https://asx.api.markitdigital.com/asx-research/1.0/companies/<TICKER>/announcements`

## Evidence / Logs

- Example (2026-02-02):
  - `[SUCCESS] ingest_announcements: 1 processed, 24 failed (218.2s)`
  - Errors included tickers such as: `AWC, BKL, BKW, DEG, DHG, IPL, ABC, MRM, NCM, OZL`.

## Cause

**Root cause confirmed:** The ASX Markit Digital API returns HTTP 400 with message "Bad Request: Symbol not found" for symbols that have been **delisted, merged, or renamed**.

Verified via direct API testing:
- `BHP` → 200 OK (active)
- `CBA` → 200 OK (active)  
- `AWC` → 400 "Symbol not found" (delisted/merged)
- `NCM` → 400 "Symbol not found" (delisted/merged)
- `ABC` → 400 "Symbol not found" (delisted/merged)

The hardcoded `ASX_300_SYMBOLS` list in `ingest_symbols.py` contains outdated symbols that no longer exist on ASX.

## Lessons Learned

- Treat announcements ingestion as an external dependency: add clearer classification/metrics for HTTP status families (2xx/4xx/5xx) and alert on sudden spikes in 4xx.
- Maintain a ticker validity filter/mapping layer (active listings, historical mappings) before calling upstream APIs.

## Feedback

- Reporter expectation (2026-02-02): some symbols may be delisted; however, this failure pattern appears systemic and should be fixed.

## Resolution

Fixed in `jobs/src/asx_jobs/jobs/ingest_announcements.py` by adding explicit handling for HTTP 400 responses:

1. **Parse 400 error body** to detect "symbol not found" message
2. **Log gracefully** as `symbol_delisted_or_invalid` instead of throwing exception
3. **Return empty list** for delisted symbols (no announcements to fetch)
4. **Distinguish** between "symbol not found" (expected for delisted) vs other 400 errors

The job will now succeed for valid symbols and gracefully skip delisted ones without counting them as failures.
