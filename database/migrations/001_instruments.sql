-- Migration: 001_instruments
-- Description: Core instruments table for ASX symbols
-- Created: 2026-01-30

CREATE TABLE IF NOT EXISTS instruments (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(255),
    sector VARCHAR(100),
    industry VARCHAR(100),
    market_cap BIGINT,
    is_asx300 BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    listed_date DATE,
    delisted_date DATE,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_instruments_symbol ON instruments(symbol);
CREATE INDEX IF NOT EXISTS idx_instruments_sector ON instruments(sector);
CREATE INDEX IF NOT EXISTS idx_instruments_is_asx300 ON instruments(is_asx300) WHERE is_asx300 = TRUE;
CREATE INDEX IF NOT EXISTS idx_instruments_is_active ON instruments(is_active) WHERE is_active = TRUE;

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER instruments_updated_at
    BEFORE UPDATE ON instruments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE instruments IS 'ASX listed instruments with metadata';
COMMENT ON COLUMN instruments.symbol IS 'ASX ticker symbol (e.g., BHP, CBA)';
COMMENT ON COLUMN instruments.is_asx300 IS 'Whether instrument is in ASX 300 index';
COMMENT ON COLUMN instruments.metadata IS 'Additional provider-specific metadata as JSON';
