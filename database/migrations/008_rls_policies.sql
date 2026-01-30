-- Migration: 008_rls_policies
-- Description: Row Level Security policies for public read-only access
-- Created: 2026-01-30

-- Enable RLS on all tables
ALTER TABLE instruments ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_prices ENABLE ROW LEVEL SECURITY;
ALTER TABLE midday_snapshots ENABLE ROW LEVEL SECURITY;
ALTER TABLE signals ENABLE ROW LEVEL SECURITY;
ALTER TABLE announcements ENABLE ROW LEVEL SECURITY;
ALTER TABLE strategies ENABLE ROW LEVEL SECURITY;
ALTER TABLE backtest_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE backtest_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE backtest_trades ENABLE ROW LEVEL SECURITY;
ALTER TABLE paper_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE paper_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE paper_positions ENABLE ROW LEVEL SECURITY;
ALTER TABLE portfolio_snapshots ENABLE ROW LEVEL SECURITY;

-- Public read-only policies (anon role can SELECT)
CREATE POLICY "Public read access for instruments"
    ON instruments FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for daily_prices"
    ON daily_prices FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for midday_snapshots"
    ON midday_snapshots FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for signals"
    ON signals FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for announcements"
    ON announcements FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for strategies"
    ON strategies FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for backtest_runs"
    ON backtest_runs FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for backtest_metrics"
    ON backtest_metrics FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for backtest_trades"
    ON backtest_trades FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for paper_accounts"
    ON paper_accounts FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for paper_orders"
    ON paper_orders FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for paper_positions"
    ON paper_positions FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for portfolio_snapshots"
    ON portfolio_snapshots FOR SELECT
    TO anon
    USING (true);

-- Service role has full access (for job runner)
-- Note: service_role bypasses RLS by default, so no explicit policies needed

COMMENT ON POLICY "Public read access for instruments" ON instruments IS 'Allow anonymous users to read instrument data';
COMMENT ON POLICY "Public read access for daily_prices" ON daily_prices IS 'Allow anonymous users to read price data';
COMMENT ON POLICY "Public read access for signals" ON signals IS 'Allow anonymous users to read signal data';
