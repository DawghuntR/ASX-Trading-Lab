-- Migration: 002_daily_prices
-- Description: Daily OHLCV price data for instruments
-- Created: 2026-01-30

CREATE TABLE IF NOT EXISTS daily_prices (
    id BIGSERIAL PRIMARY KEY,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    trade_date DATE NOT NULL,
    open DECIMAL(12, 4),
    high DECIMAL(12, 4),
    low DECIMAL(12, 4),
    close DECIMAL(12, 4) NOT NULL,
    adjusted_close DECIMAL(12, 4),
    volume BIGINT DEFAULT 0,
    turnover DECIMAL(18, 2),
    trades_count INTEGER,
    data_source VARCHAR(50) DEFAULT 'yahoo',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT uq_daily_prices_instrument_date UNIQUE (instrument_id, trade_date)
);

-- Indexes for performant queries
CREATE INDEX IF NOT EXISTS idx_daily_prices_instrument_id ON daily_prices(instrument_id);
CREATE INDEX IF NOT EXISTS idx_daily_prices_trade_date ON daily_prices(trade_date DESC);
CREATE INDEX IF NOT EXISTS idx_daily_prices_instrument_date ON daily_prices(instrument_id, trade_date DESC);

-- Composite index for date range queries
CREATE INDEX IF NOT EXISTS idx_daily_prices_date_range 
    ON daily_prices(instrument_id, trade_date) 
    INCLUDE (open, high, low, close, volume);

COMMENT ON TABLE daily_prices IS 'End-of-day OHLCV price data';
COMMENT ON COLUMN daily_prices.adjusted_close IS 'Close price adjusted for splits and dividends';
COMMENT ON COLUMN daily_prices.turnover IS 'Total dollar value traded';
COMMENT ON COLUMN daily_prices.data_source IS 'Provider source (yahoo, asx, etc.)';
