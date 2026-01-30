---
id: 015
name: Data Quality & Observability
status: Completed
completed: 2026-01-31
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

- Prevents "silent failure" and makes the platform maintainable.

## Success Criteria

- Each daily run produces a run record.
- UI can show: last successful run time, number of symbols updated, failures.
- Stale data is detectable and reportable.

## Implementation Details

### Database (Migration 011)

- `job_runs` table - stores execution metadata for each job
- `data_quality_checks` table - records data quality issues
- Enhanced `get_ingest_status()` function - now returns `last_successful_run`, `days_since_update`, `unresolved_issues`
- New views: `v_job_run_summary`, `v_latest_job_runs`, `v_stale_data_check`, `v_price_quality_issues`, `v_unresolved_quality_issues`
- New function: `get_job_run_stats(p_days)` - aggregated job statistics

### Python Backend

- `asx_jobs/observability.py` - JobRunTracker and DataQualityMonitor classes
- Orchestrator integration - automatic job run tracking and quality checks after daily runs

### Frontend

- `/health` page - System health dashboard with job stats and quality issues
- New API module and hooks for observability data
- Enhanced IngestStatus interface with new fields
