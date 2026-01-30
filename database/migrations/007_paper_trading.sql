-- Migration: 007_paper_trading
-- Description: Paper trading ledger for simulated trading
-- Created: 2026-01-30

-- Order status enum
CREATE TYPE order_status AS ENUM (
    'pending',
    'filled',
    'partial',
    'cancelled',
    'rejected'
);

-- Order side enum
CREATE TYPE order_side AS ENUM (
    'buy',
    'sell'
);

-- Order type enum
CREATE TYPE order_type AS ENUM (
    'market',
    'limit',
    'stop',
    'stop_limit'
);

-- Paper trading accounts
CREATE TABLE IF NOT EXISTS paper_accounts (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    initial_balance DECIMAL(14, 2) NOT NULL DEFAULT 100000,
    cash_balance DECIMAL(14, 2) NOT NULL DEFAULT 100000,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TRIGGER paper_accounts_updated_at
    BEFORE UPDATE ON paper_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Paper trading orders
CREATE TABLE IF NOT EXISTS paper_orders (
    id BIGSERIAL PRIMARY KEY,
    account_id BIGINT NOT NULL REFERENCES paper_accounts(id) ON DELETE CASCADE,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    order_side order_side NOT NULL,
    order_type order_type NOT NULL DEFAULT 'market',
    quantity INTEGER NOT NULL,
    limit_price DECIMAL(12, 4),
    stop_price DECIMAL(12, 4),
    filled_quantity INTEGER DEFAULT 0,
    filled_avg_price DECIMAL(12, 4),
    status order_status DEFAULT 'pending',
    submitted_at TIMESTAMPTZ DEFAULT NOW(),
    filled_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_paper_orders_account ON paper_orders(account_id);
CREATE INDEX IF NOT EXISTS idx_paper_orders_instrument ON paper_orders(instrument_id);
CREATE INDEX IF NOT EXISTS idx_paper_orders_status ON paper_orders(status);
CREATE INDEX IF NOT EXISTS idx_paper_orders_submitted ON paper_orders(submitted_at DESC);

-- Paper trading positions
CREATE TABLE IF NOT EXISTS paper_positions (
    id BIGSERIAL PRIMARY KEY,
    account_id BIGINT NOT NULL REFERENCES paper_accounts(id) ON DELETE CASCADE,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0,
    avg_entry_price DECIMAL(12, 4) NOT NULL,
    current_price DECIMAL(12, 4),
    unrealized_pnl DECIMAL(14, 4),
    realized_pnl DECIMAL(14, 4) DEFAULT 0,
    opened_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT uq_paper_positions_account_instrument UNIQUE (account_id, instrument_id)
);

CREATE TRIGGER paper_positions_updated_at
    BEFORE UPDATE ON paper_positions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE INDEX IF NOT EXISTS idx_paper_positions_account ON paper_positions(account_id);
CREATE INDEX IF NOT EXISTS idx_paper_positions_instrument ON paper_positions(instrument_id);

-- Portfolio snapshots for tracking value over time
CREATE TABLE IF NOT EXISTS portfolio_snapshots (
    id BIGSERIAL PRIMARY KEY,
    account_id BIGINT NOT NULL REFERENCES paper_accounts(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    cash_balance DECIMAL(14, 2) NOT NULL,
    positions_value DECIMAL(14, 2) NOT NULL,
    total_value DECIMAL(14, 2) NOT NULL,
    daily_pnl DECIMAL(14, 2),
    daily_return DECIMAL(10, 6),
    positions_snapshot JSONB DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT uq_portfolio_snapshots_account_date UNIQUE (account_id, snapshot_date)
);

CREATE INDEX IF NOT EXISTS idx_portfolio_snapshots_account ON portfolio_snapshots(account_id);
CREATE INDEX IF NOT EXISTS idx_portfolio_snapshots_date ON portfolio_snapshots(snapshot_date DESC);
CREATE INDEX IF NOT EXISTS idx_portfolio_snapshots_account_date ON portfolio_snapshots(account_id, snapshot_date DESC);

COMMENT ON TABLE paper_accounts IS 'Paper trading accounts for simulated trading';
COMMENT ON TABLE paper_orders IS 'Paper trading order ledger';
COMMENT ON TABLE paper_positions IS 'Current paper trading positions';
COMMENT ON TABLE portfolio_snapshots IS 'Daily portfolio value snapshots for performance tracking';
