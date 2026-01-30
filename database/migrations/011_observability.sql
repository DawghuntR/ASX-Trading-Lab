-- Migration: 011_observability
-- Description: Job run tracking and data quality monitoring tables
-- Created: 2026-01-31
-- Feature: 015 - Data Quality & Observability

-- ============================================================================
-- Table: job_runs - Track job execution history
-- ============================================================================
CREATE TABLE IF NOT EXISTS job_runs (
    id BIGSERIAL PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL,
    run_date DATE NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL CHECK (status IN ('success', 'partial_failure', 'failure')),
    records_processed INTEGER DEFAULT 0,
    records_failed INTEGER DEFAULT 0,
    duration_seconds NUMERIC(10, 2),
    error_message TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_job_runs_job_name_date ON job_runs (job_name, run_date DESC);
CREATE INDEX IF NOT EXISTS idx_job_runs_run_date ON job_runs (run_date DESC);
CREATE INDEX IF NOT EXISTS idx_job_runs_status ON job_runs (status);

COMMENT ON TABLE job_runs IS 'Tracks execution history for all automated jobs';
COMMENT ON COLUMN job_runs.job_name IS 'Name of the job (e.g., ingest_symbols, ingest_prices)';
COMMENT ON COLUMN job_runs.status IS 'Execution outcome: success, partial_failure, or failure';
COMMENT ON COLUMN job_runs.metadata IS 'Additional job-specific execution details';

-- ============================================================================
-- Table: data_quality_checks - Track data quality issues
-- ============================================================================
CREATE TABLE IF NOT EXISTS data_quality_checks (
    id BIGSERIAL PRIMARY KEY,
    check_date DATE NOT NULL,
    check_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL CHECK (severity IN ('info', 'warning', 'error')),
    affected_count INTEGER DEFAULT 0,
    affected_symbols TEXT[] DEFAULT '{}',
    description TEXT,
    details JSONB DEFAULT '{}',
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_data_quality_checks_date_type ON data_quality_checks (check_date DESC, check_type);
CREATE INDEX IF NOT EXISTS idx_data_quality_checks_unresolved ON data_quality_checks (resolved_at) WHERE resolved_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_data_quality_checks_severity ON data_quality_checks (severity);

COMMENT ON TABLE data_quality_checks IS 'Records data quality issues detected during monitoring';
COMMENT ON COLUMN data_quality_checks.check_type IS 'Type: stale_data, missing_snapshot, null_prices, abnormal_values';
COMMENT ON COLUMN data_quality_checks.severity IS 'Issue severity: info, warning, or error';
COMMENT ON COLUMN data_quality_checks.affected_symbols IS 'Array of affected ticker symbols';
COMMENT ON COLUMN data_quality_checks.resolved_at IS 'When the issue was resolved (NULL if still active)';

-- ============================================================================
-- View: v_job_run_summary - Recent job health overview
-- ============================================================================
CREATE OR REPLACE VIEW v_job_run_summary AS
SELECT 
    job_name,
    run_date,
    status,
    records_processed,
    records_failed,
    duration_seconds,
    error_message,
    started_at,
    completed_at,
    ROW_NUMBER() OVER (PARTITION BY job_name ORDER BY run_date DESC, started_at DESC) AS run_rank
FROM job_runs
ORDER BY run_date DESC, started_at DESC;

COMMENT ON VIEW v_job_run_summary IS 'Summary of job runs with ranking for each job type';

-- ============================================================================
-- View: v_latest_job_runs - Most recent run for each job
-- ============================================================================
CREATE OR REPLACE VIEW v_latest_job_runs AS
SELECT DISTINCT ON (job_name)
    job_name,
    run_date,
    status,
    records_processed,
    records_failed,
    duration_seconds,
    error_message,
    started_at,
    completed_at
FROM job_runs
ORDER BY job_name, run_date DESC, started_at DESC;

COMMENT ON VIEW v_latest_job_runs IS 'Most recent run for each job type';

-- ============================================================================
-- View: v_stale_data_check - Symbols without recent price data
-- ============================================================================
CREATE OR REPLACE VIEW v_stale_data_check AS
SELECT 
    i.id,
    i.symbol,
    i.name,
    MAX(dp.trade_date) AS last_price_date,
    CURRENT_DATE - MAX(dp.trade_date) AS days_since_update,
    CASE 
        WHEN MAX(dp.trade_date) IS NULL THEN 'never'
        WHEN CURRENT_DATE - MAX(dp.trade_date) >= 7 THEN 'stale'
        WHEN CURRENT_DATE - MAX(dp.trade_date) >= 3 THEN 'warning'
        ELSE 'current'
    END AS staleness_status
FROM instruments i
LEFT JOIN daily_prices dp ON i.id = dp.instrument_id
WHERE i.is_active = TRUE
GROUP BY i.id, i.symbol, i.name
ORDER BY days_since_update DESC NULLS FIRST;

COMMENT ON VIEW v_stale_data_check IS 'Identifies symbols with stale or missing price data';

-- ============================================================================
-- View: v_price_quality_issues - Abnormal or invalid price values
-- ============================================================================
CREATE OR REPLACE VIEW v_price_quality_issues AS
SELECT 
    i.symbol,
    i.name,
    dp.trade_date,
    dp.open,
    dp.high,
    dp.low,
    dp.close,
    dp.volume,
    CASE
        WHEN dp.close IS NULL OR dp.close <= 0 THEN 'null_or_zero_close'
        WHEN dp.high < dp.low THEN 'invalid_high_low_range'
        WHEN dp.open IS NULL OR dp.open <= 0 THEN 'null_or_zero_open'
        WHEN dp.close > dp.high THEN 'close_exceeds_high'
        WHEN dp.close < dp.low THEN 'close_below_low'
        ELSE 'unknown'
    END AS issue_type
FROM instruments i
JOIN daily_prices dp ON i.id = dp.instrument_id
WHERE i.is_active = TRUE
  AND (
      dp.close IS NULL 
      OR dp.close <= 0 
      OR dp.high < dp.low 
      OR dp.close > dp.high 
      OR dp.close < dp.low
      OR dp.open IS NULL
      OR dp.open <= 0
  )
ORDER BY dp.trade_date DESC;

COMMENT ON VIEW v_price_quality_issues IS 'Identifies price records with data quality problems';

-- ============================================================================
-- View: v_unresolved_quality_issues - Active data quality issues
-- ============================================================================
CREATE OR REPLACE VIEW v_unresolved_quality_issues AS
SELECT 
    id,
    check_date,
    check_type,
    severity,
    affected_count,
    affected_symbols,
    description,
    details,
    created_at
FROM data_quality_checks
WHERE resolved_at IS NULL
ORDER BY 
    CASE severity 
        WHEN 'error' THEN 1 
        WHEN 'warning' THEN 2 
        ELSE 3 
    END,
    check_date DESC;

COMMENT ON VIEW v_unresolved_quality_issues IS 'Active data quality issues requiring attention';

-- ============================================================================
-- Function: get_ingest_status (Enhanced)
-- Updates the existing function to include job run information
-- ============================================================================
CREATE OR REPLACE FUNCTION get_ingest_status()
RETURNS TABLE (
    total_instruments BIGINT,
    active_instruments BIGINT,
    asx300_instruments BIGINT,
    latest_price_date DATE,
    prices_today BIGINT,
    signals_today BIGINT,
    last_successful_run TIMESTAMPTZ,
    days_since_update INTEGER,
    unresolved_issues BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*) FROM instruments)::BIGINT AS total_instruments,
        (SELECT COUNT(*) FROM instruments WHERE is_active = TRUE)::BIGINT AS active_instruments,
        (SELECT COUNT(*) FROM instruments WHERE is_asx300 = TRUE)::BIGINT AS asx300_instruments,
        (SELECT MAX(trade_date) FROM daily_prices) AS latest_price_date,
        (SELECT COUNT(*) FROM daily_prices WHERE trade_date = CURRENT_DATE)::BIGINT AS prices_today,
        (SELECT COUNT(*) FROM signals WHERE signal_date = CURRENT_DATE)::BIGINT AS signals_today,
        (SELECT MAX(completed_at) FROM job_runs WHERE status = 'success') AS last_successful_run,
        (SELECT COALESCE(CURRENT_DATE - MAX(trade_date), 999) FROM daily_prices)::INTEGER AS days_since_update,
        (SELECT COUNT(*) FROM data_quality_checks WHERE resolved_at IS NULL)::BIGINT AS unresolved_issues;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_ingest_status IS 'Get comprehensive data ingestion and health status';

-- ============================================================================
-- Function: get_job_run_stats - Aggregated job statistics
-- ============================================================================
CREATE OR REPLACE FUNCTION get_job_run_stats(p_days INTEGER DEFAULT 30)
RETURNS TABLE (
    job_name VARCHAR(100),
    total_runs BIGINT,
    successful_runs BIGINT,
    failed_runs BIGINT,
    success_rate NUMERIC(5, 2),
    avg_duration_seconds NUMERIC(10, 2),
    avg_records_processed NUMERIC(10, 2),
    last_run_at TIMESTAMPTZ,
    last_run_status VARCHAR(20)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        jr.job_name,
        COUNT(*)::BIGINT AS total_runs,
        COUNT(*) FILTER (WHERE jr.status = 'success')::BIGINT AS successful_runs,
        COUNT(*) FILTER (WHERE jr.status = 'failure')::BIGINT AS failed_runs,
        ROUND(
            (COUNT(*) FILTER (WHERE jr.status = 'success')::NUMERIC / NULLIF(COUNT(*), 0)) * 100, 
            2
        ) AS success_rate,
        ROUND(AVG(jr.duration_seconds), 2) AS avg_duration_seconds,
        ROUND(AVG(jr.records_processed), 2) AS avg_records_processed,
        MAX(jr.completed_at) AS last_run_at,
        (
            SELECT status FROM job_runs jr2 
            WHERE jr2.job_name = jr.job_name 
            ORDER BY jr2.run_date DESC, jr2.started_at DESC 
            LIMIT 1
        ) AS last_run_status
    FROM job_runs jr
    WHERE jr.run_date >= CURRENT_DATE - p_days
    GROUP BY jr.job_name
    ORDER BY jr.job_name;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION get_job_run_stats IS 'Get aggregated job execution statistics';

-- ============================================================================
-- RLS Policies for new tables (public read access)
-- ============================================================================

-- Enable RLS
ALTER TABLE job_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE data_quality_checks ENABLE ROW LEVEL SECURITY;

-- Public read access (consistent with other tables)
CREATE POLICY "Allow public read access on job_runs"
    ON job_runs FOR SELECT
    USING (true);

CREATE POLICY "Allow public read access on data_quality_checks"
    ON data_quality_checks FOR SELECT
    USING (true);

-- Service role write access (for jobs runner)
CREATE POLICY "Allow service role insert on job_runs"
    ON job_runs FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Allow service role insert on data_quality_checks"
    ON data_quality_checks FOR INSERT
    WITH CHECK (true);

CREATE POLICY "Allow service role update on data_quality_checks"
    ON data_quality_checks FOR UPDATE
    USING (true);
