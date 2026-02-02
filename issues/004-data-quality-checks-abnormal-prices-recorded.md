---
id: 004
title: data_quality_checks records abnormal_prices errors
status: Closed
priority: Low
component: jobs/data_quality_checks
date_reported: 2026-02-02
date_closed: 2026-02-02
resolution: By Design
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

**Confirmed:** The data quality monitoring system is working as designed. The check detects OHLC price anomalies:

- `null_or_zero_close` - Missing or zero close price
- `invalid_high_low_range` - High price less than low price
- `null_or_zero_open` - Missing or zero open price
- `close_exceeds_high` - Close price higher than high
- `close_below_low` - Close price lower than low

Severity is set to `error` when `affected_count > 10`, which is correct behavior.

The 13 anomalies likely come from:
- Yahoo Finance returning malformed OHLC data for some symbols
- Edge cases in newly listed or thinly traded stocks
- Corporate actions (splits, etc.) not yet adjusted

## Lessons Learned

- Ensure quality checks are actionable: link recorded issues to concrete example rows and provide a runbook for investigation.
- Consider separate severities for "requires investigation" vs "known expected anomalies".

## Resolution

**Closed as "By Design"** - The quality monitoring system is working correctly:

1. **Detection working:** Correctly identified 13 price records with OHLC anomalies
2. **Severity correct:** `error` severity appropriate for count > 10
3. **Non-blocking:** Quality checks are informational; they log issues but don't fail the job
4. **Feature compliant:** Matches Feature 015 specification for data quality monitoring

This is the quality system **alerting you to investigate**, not a bug in the system itself.

**To investigate the underlying data anomalies**, run:
```sql
SELECT details->'issue_breakdown', affected_symbols, check_date
FROM data_quality_checks 
WHERE check_type = 'abnormal_prices'
ORDER BY check_date DESC LIMIT 5;
```

**No code fix required.** The quality monitoring is doing its job correctly.
