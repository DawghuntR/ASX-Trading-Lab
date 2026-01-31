BEGIN;

-- Job run logs: keep 90 days
DELETE FROM job_runs
WHERE created_at < NOW() - INTERVAL '90 days';

-- Data quality issues: resolved > 90 days, unresolved > 1 year
DELETE FROM data_quality_issues
WHERE resolved_at IS NOT NULL
  AND resolved_at < NOW() - INTERVAL '90 days';

DELETE FROM data_quality_issues
WHERE resolved_at IS NULL
  AND created_at < NOW() - INTERVAL '1 year';

-- Signals: keep 2 years
DELETE FROM signals
WHERE created_at < NOW() - INTERVAL '2 years';

-- Backtests: optional cleanup (uncomment after review)
-- DELETE FROM backtest_trades
-- WHERE created_at < NOW() - INTERVAL '1 year';
-- DELETE FROM backtest_runs
-- WHERE created_at < NOW() - INTERVAL '1 year';

COMMIT;

-- Run this after cleanup to reclaim space
-- VACUUM ANALYZE;
