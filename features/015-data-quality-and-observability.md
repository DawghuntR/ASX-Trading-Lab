---
id: 015
name: Data Quality & Observability
status: Planned
---

# 015 - Data Quality & Observability

Add visibility into job runs, coverage, and data freshness so the system is trustworthy.

## Description

- Persist job run metadata (start/end, status, counts, errors).
- Implement basic data quality checks:
  - stale data detection (no updates within last week)
  - missing snapshot for symbols
  - abnormal/null price values
- Provide UI surfacing for ingest health.

## Impact

- Prevents “silent failure” and makes the platform maintainable.

## Success Criteria

- Each daily run produces a run record.
- UI can show: last successful run time, number of symbols updated, failures.
- Stale data is detectable and reportable.
