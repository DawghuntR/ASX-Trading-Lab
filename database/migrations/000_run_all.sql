-- Master Migration Script
-- Run all migrations in order for ASX Trading Lab
-- 
-- Usage in Supabase SQL Editor:
--   Copy and paste this entire file, or run each migration file individually
--
-- Migration Order:
--   001_instruments.sql       - Core instruments table
--   002_daily_prices.sql      - Daily OHLCV data
--   003_midday_snapshots.sql  - Intraday snapshots
--   004_signals.sql           - Trading signals
--   005_announcements.sql     - ASX announcements
--   006_backtests.sql         - Backtesting tables
--   007_paper_trading.sql     - Paper trading ledger
--   008_rls_policies.sql      - Row Level Security
--   009_views.sql             - Convenience views
--   010_functions.sql         - Utility functions
--   011_observability.sql     - Job runs and data quality tracking
--   012_announcement_reactions.sql - News reaction analytics
--   013_provider_mappings.sql - Symbol normalization and provider mappings
--   014_performance_indexes.sql - Performance optimization indexes

-- To run: Execute each migration file in the Supabase SQL Editor
-- Or concatenate all files and run as a single transaction:

BEGIN;

-- Run migrations here by pasting content from each file
-- Or use Supabase CLI: supabase db push

COMMIT;
