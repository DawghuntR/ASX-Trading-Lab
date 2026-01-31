-- Migration: 014_performance_indexes
-- Description: Performance optimization indexes for common query patterns
-- Created: 2026-01-31
-- Related: Feature 038 - Performance & Rate-Limit Management

-- ============================================================================
-- DAILY PRICES INDEXES
-- These support the most common queries: latest prices, date ranges, symbol lookups
-- ============================================================================

-- Composite index for instrument + date range queries (most common pattern)
CREATE INDEX IF NOT EXISTS idx_daily_prices_instrument_date_desc 
    ON daily_prices(instrument_id, trade_date DESC);

-- Index for finding latest trade date quickly
CREATE INDEX IF NOT EXISTS idx_daily_prices_trade_date_desc 
    ON daily_prices(trade_date DESC);

-- Covering index for price lookups (includes commonly selected columns)
CREATE INDEX IF NOT EXISTS idx_daily_prices_covering 
    ON daily_prices(instrument_id, trade_date DESC) 
    INCLUDE (open, high, low, close, volume);

-- ============================================================================
-- SIGNALS INDEXES
-- Support filtering by date, type, and direction
-- ============================================================================

-- Composite index for date + type filtering (dashboard queries)
CREATE INDEX IF NOT EXISTS idx_signals_date_type 
    ON signals(signal_date DESC, signal_type);

-- Index for instrument signal history
CREATE INDEX IF NOT EXISTS idx_signals_instrument_date 
    ON signals(instrument_id, signal_date DESC);

-- Index for recent signals sorted by date and strength
-- Note: Cannot use partial index with CURRENT_DATE (not immutable)
-- The query planner will use this index efficiently for date-range queries
CREATE INDEX IF NOT EXISTS idx_signals_date_strength 
    ON signals(signal_date DESC, signal_strength DESC NULLS LAST);

-- ============================================================================
-- ANNOUNCEMENTS INDEXES
-- Support chronological browsing and instrument lookups
-- ============================================================================

-- Index for chronological announcement browsing
CREATE INDEX IF NOT EXISTS idx_announcements_announced_at_desc 
    ON announcements(announced_at DESC);

-- Index for instrument announcement history
CREATE INDEX IF NOT EXISTS idx_announcements_instrument_date 
    ON announcements(instrument_id, announced_at DESC);

-- ============================================================================
-- BACKTEST INDEXES
-- Support leaderboard and trade history queries
-- ============================================================================

-- Index for backtest leaderboard (completed runs)
CREATE INDEX IF NOT EXISTS idx_backtest_runs_completed 
    ON backtest_runs(status, completed_at DESC) 
    WHERE status = 'completed';

-- Index for trade history queries
CREATE INDEX IF NOT EXISTS idx_backtest_trades_run_date 
    ON backtest_trades(backtest_run_id, entry_date);

-- ============================================================================
-- PAPER TRADING INDEXES
-- Support portfolio and order queries
-- ============================================================================

-- Index for active positions
CREATE INDEX IF NOT EXISTS idx_paper_positions_active 
    ON paper_positions(account_id, instrument_id) 
    WHERE quantity > 0;

-- Index for pending orders
CREATE INDEX IF NOT EXISTS idx_paper_orders_pending 
    ON paper_orders(account_id, status, created_at DESC) 
    WHERE status = 'pending';

-- ============================================================================
-- JOB RUNS INDEXES (Observability)
-- Support health checks and troubleshooting
-- Note: Only created if job_runs table exists (from migration 011)
-- ============================================================================

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'job_runs') THEN
        CREATE INDEX IF NOT EXISTS idx_job_runs_recent 
            ON job_runs(job_name, started_at DESC);
        CREATE INDEX IF NOT EXISTS idx_job_runs_failed 
            ON job_runs(status, started_at DESC) 
            WHERE status = 'failure';
    END IF;
END $$;

-- ============================================================================
-- DATA QUALITY INDEXES
-- Support unresolved issues lookup
-- Note: Only created if data_quality_issues table exists (from migration 011)
-- ============================================================================

DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'data_quality_issues') THEN
        CREATE INDEX IF NOT EXISTS idx_data_quality_unresolved 
            ON data_quality_issues(check_type, check_date DESC) 
            WHERE resolved_at IS NULL;
    END IF;
END $$;

-- ============================================================================
-- STATISTICS AND MAINTENANCE
-- ============================================================================

-- Update table statistics for query planner
ANALYZE instruments;
ANALYZE daily_prices;
ANALYZE signals;
ANALYZE announcements;
ANALYZE backtest_runs;
ANALYZE backtest_trades;
ANALYZE paper_accounts;
ANALYZE paper_positions;
ANALYZE paper_orders;

-- Comments
COMMENT ON INDEX idx_daily_prices_instrument_date_desc IS 'Optimizes symbol price history queries';
COMMENT ON INDEX idx_daily_prices_covering IS 'Covering index to avoid table lookups for common price queries';
COMMENT ON INDEX idx_signals_date_strength IS 'Index for signals sorted by date and strength - supports dashboard queries';
