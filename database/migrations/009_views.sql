-- Migration: 009_views
-- Description: Convenience views for common queries
-- Created: 2026-01-30

-- View: Latest prices with instrument info
CREATE OR REPLACE VIEW v_latest_prices AS
SELECT 
    i.id AS instrument_id,
    i.symbol,
    i.name,
    i.sector,
    i.is_asx300,
    dp.trade_date,
    dp.open,
    dp.high,
    dp.low,
    dp.close,
    dp.adjusted_close,
    dp.volume,
    dp.turnover,
    ROUND(((dp.close - LAG(dp.close) OVER (PARTITION BY i.id ORDER BY dp.trade_date)) / 
           NULLIF(LAG(dp.close) OVER (PARTITION BY i.id ORDER BY dp.trade_date), 0)) * 100, 2) AS change_percent
FROM instruments i
JOIN daily_prices dp ON i.id = dp.instrument_id
WHERE dp.trade_date = (SELECT MAX(trade_date) FROM daily_prices)
  AND i.is_active = TRUE;

-- View: Today's signals with instrument info
CREATE OR REPLACE VIEW v_todays_signals AS
SELECT 
    i.symbol,
    i.name,
    s.signal_date,
    s.signal_type,
    s.signal_direction,
    s.signal_strength,
    s.value,
    s.description,
    dp.close AS current_price,
    dp.volume
FROM signals s
JOIN instruments i ON s.instrument_id = i.id
LEFT JOIN daily_prices dp ON s.instrument_id = dp.instrument_id 
    AND dp.trade_date = s.signal_date
WHERE s.signal_date = CURRENT_DATE
ORDER BY s.signal_strength DESC NULLS LAST;

-- View: Price movers (top gainers/losers)
CREATE OR REPLACE VIEW v_price_movers AS
WITH latest_prices AS (
    SELECT 
        instrument_id,
        trade_date,
        close,
        LAG(close) OVER (PARTITION BY instrument_id ORDER BY trade_date) AS prev_close
    FROM daily_prices
    WHERE trade_date >= CURRENT_DATE - INTERVAL '5 days'
),
price_changes AS (
    SELECT 
        instrument_id,
        trade_date,
        close,
        prev_close,
        ROUND(((close - prev_close) / NULLIF(prev_close, 0)) * 100, 2) AS change_percent
    FROM latest_prices
    WHERE prev_close IS NOT NULL
)
SELECT 
    i.symbol,
    i.name,
    i.sector,
    pc.trade_date,
    pc.close,
    pc.prev_close,
    pc.change_percent
FROM price_changes pc
JOIN instruments i ON pc.instrument_id = i.id
WHERE pc.trade_date = (SELECT MAX(trade_date) FROM daily_prices)
  AND i.is_active = TRUE
ORDER BY ABS(pc.change_percent) DESC;

-- View: Backtest leaderboard
CREATE OR REPLACE VIEW v_backtest_leaderboard AS
SELECT 
    s.name AS strategy_name,
    br.name AS run_name,
    br.start_date,
    br.end_date,
    br.initial_capital,
    br.final_capital,
    bm.total_return,
    bm.annualized_return,
    bm.sharpe_ratio,
    bm.max_drawdown,
    bm.win_rate,
    bm.total_trades,
    br.completed_at
FROM backtest_runs br
JOIN strategies s ON br.strategy_id = s.id
LEFT JOIN backtest_metrics bm ON br.id = bm.backtest_run_id
WHERE br.status = 'completed'
ORDER BY bm.sharpe_ratio DESC NULLS LAST;

-- View: Portfolio summary
CREATE OR REPLACE VIEW v_portfolio_summary AS
SELECT 
    pa.id AS account_id,
    pa.name AS account_name,
    pa.initial_balance,
    pa.cash_balance,
    COALESCE(SUM(pp.quantity * pp.current_price), 0) AS positions_value,
    pa.cash_balance + COALESCE(SUM(pp.quantity * pp.current_price), 0) AS total_value,
    ROUND(((pa.cash_balance + COALESCE(SUM(pp.quantity * pp.current_price), 0) - pa.initial_balance) 
           / pa.initial_balance) * 100, 2) AS total_return_percent,
    COUNT(pp.id) AS open_positions
FROM paper_accounts pa
LEFT JOIN paper_positions pp ON pa.id = pp.account_id AND pp.quantity > 0
WHERE pa.is_active = TRUE
GROUP BY pa.id, pa.name, pa.initial_balance, pa.cash_balance;

-- View: Ingest health status
CREATE OR REPLACE VIEW v_ingest_health AS
SELECT 
    'daily_prices' AS data_type,
    MAX(trade_date) AS latest_date,
    COUNT(DISTINCT instrument_id) AS instruments_covered,
    COUNT(*) AS total_records,
    MAX(created_at) AS last_ingest_at
FROM daily_prices
UNION ALL
SELECT 
    'midday_snapshots' AS data_type,
    MAX(snapshot_date) AS latest_date,
    COUNT(DISTINCT instrument_id) AS instruments_covered,
    COUNT(*) AS total_records,
    MAX(created_at) AS last_ingest_at
FROM midday_snapshots
UNION ALL
SELECT 
    'signals' AS data_type,
    MAX(signal_date) AS latest_date,
    COUNT(DISTINCT instrument_id) AS instruments_covered,
    COUNT(*) AS total_records,
    MAX(created_at) AS last_ingest_at
FROM signals
UNION ALL
SELECT 
    'announcements' AS data_type,
    MAX(announced_at::date) AS latest_date,
    COUNT(DISTINCT instrument_id) AS instruments_covered,
    COUNT(*) AS total_records,
    MAX(created_at) AS last_ingest_at
FROM announcements;

COMMENT ON VIEW v_latest_prices IS 'Latest daily prices with instrument info and daily change';
COMMENT ON VIEW v_todays_signals IS 'All signals generated for current date';
COMMENT ON VIEW v_price_movers IS 'Top price movers (gainers and losers)';
COMMENT ON VIEW v_backtest_leaderboard IS 'Ranked backtest results by Sharpe ratio';
COMMENT ON VIEW v_portfolio_summary IS 'Paper trading portfolio summary';
COMMENT ON VIEW v_ingest_health IS 'Data ingestion health status';
