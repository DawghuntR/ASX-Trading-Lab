-- Migration: 006_backtests
-- Description: Backtesting engine tables for strategies, runs, and trades
-- Created: 2026-01-30

-- Strategy definitions
CREATE TABLE IF NOT EXISTS strategies (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    version VARCHAR(20) DEFAULT '1.0.0',
    parameters JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER strategies_updated_at
    BEFORE UPDATE ON strategies
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Backtest runs
CREATE TABLE IF NOT EXISTS backtest_runs (
    id BIGSERIAL PRIMARY KEY,
    strategy_id BIGINT NOT NULL REFERENCES strategies(id) ON DELETE CASCADE,
    name VARCHAR(255),
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    initial_capital DECIMAL(14, 2) NOT NULL DEFAULT 100000,
    final_capital DECIMAL(14, 2),
    parameters JSONB DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    error_message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_backtest_runs_strategy ON backtest_runs(strategy_id);
CREATE INDEX IF NOT EXISTS idx_backtest_runs_status ON backtest_runs(status);
CREATE INDEX IF NOT EXISTS idx_backtest_runs_created ON backtest_runs(created_at DESC);

-- Backtest metrics summary
CREATE TABLE IF NOT EXISTS backtest_metrics (
    id BIGSERIAL PRIMARY KEY,
    backtest_run_id BIGINT NOT NULL REFERENCES backtest_runs(id) ON DELETE CASCADE,
    total_return DECIMAL(10, 4),
    annualized_return DECIMAL(10, 4),
    sharpe_ratio DECIMAL(8, 4),
    sortino_ratio DECIMAL(8, 4),
    max_drawdown DECIMAL(10, 4),
    max_drawdown_duration INTEGER,
    win_rate DECIMAL(6, 4),
    profit_factor DECIMAL(8, 4),
    total_trades INTEGER DEFAULT 0,
    winning_trades INTEGER DEFAULT 0,
    losing_trades INTEGER DEFAULT 0,
    avg_win DECIMAL(12, 4),
    avg_loss DECIMAL(12, 4),
    largest_win DECIMAL(12, 4),
    largest_loss DECIMAL(12, 4),
    avg_holding_period_days DECIMAL(8, 2),
    exposure_time DECIMAL(6, 4),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT uq_backtest_metrics_run UNIQUE (backtest_run_id)
);

-- Backtest trades
CREATE TABLE IF NOT EXISTS backtest_trades (
    id BIGSERIAL PRIMARY KEY,
    backtest_run_id BIGINT NOT NULL REFERENCES backtest_runs(id) ON DELETE CASCADE,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    entry_date DATE NOT NULL,
    entry_price DECIMAL(12, 4) NOT NULL,
    exit_date DATE,
    exit_price DECIMAL(12, 4),
    quantity INTEGER NOT NULL,
    side VARCHAR(10) NOT NULL,
    pnl DECIMAL(14, 4),
    pnl_percent DECIMAL(10, 4),
    exit_reason VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_backtest_trades_run ON backtest_trades(backtest_run_id);
CREATE INDEX IF NOT EXISTS idx_backtest_trades_instrument ON backtest_trades(instrument_id);
CREATE INDEX IF NOT EXISTS idx_backtest_trades_entry_date ON backtest_trades(entry_date);

COMMENT ON TABLE strategies IS 'Trading strategy definitions';
COMMENT ON TABLE backtest_runs IS 'Individual backtest execution runs';
COMMENT ON TABLE backtest_metrics IS 'Summary performance metrics for each backtest';
COMMENT ON TABLE backtest_trades IS 'Individual trades executed during backtest';
