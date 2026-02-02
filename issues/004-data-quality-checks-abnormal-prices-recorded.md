---
id: 004
title: data_quality_checks records abnormal_prices errors
status: Open
priority: Low
component: jobs/data_quality_checks
date_reported: 2026-02-02
---

# 004 - data_quality_checks records abnormal_prices errors

During the daily orchestrator run, `data_quality_checks` recorded `abnormal_prices` with `severity=error` affecting multiple records.

## Impact

- Indicates potential data anomalies in stored prices.
- If these are true anomalies, analytics and signals may be distorted; if false positives, alert noise increases.

## Steps to Reproduce

1. Run the daily jobs (example): `asx-jobs daily`.
2. Observe the data quality check logs.
3. Confirm events such as `data_quality_issue_recorded` for `check_type=abnormal_prices`.

## Evidence / Logs

- Example (2026-02-02):
  - `{"check_type": "abnormal_prices", "severity": "error", "affected_count": 13, "issue_id": 2, ...}`
  - `{"issues_found": 13, "event": "price_quality_check_completed", ...}`
  - `{"total_issues": 235, "event": "data_quality_checks_completed", ...}`

## Cause

TBD.

Possibilities:
- Genuine price anomalies (splits, bad prints, stale values).
- Thresholds too tight for certain illiquid symbols.
- Missing corporate-actions adjustment.

## Lessons Learned

- Ensure quality checks are actionable: link recorded issues to concrete example rows and provide a runbook for investigation.
- Consider separate severities for “requires investigation” vs “known expected anomalies”.
