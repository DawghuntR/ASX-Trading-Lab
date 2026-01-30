-- Migration: 003_midday_snapshots
-- Description: Intraday price snapshots captured at midday Sydney time
-- Created: 2026-01-30

CREATE TABLE IF NOT EXISTS midday_snapshots (
    id BIGSERIAL PRIMARY KEY,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    snapshot_time TIMETZ NOT NULL,
    price DECIMAL(12, 4) NOT NULL,
    change_from_open DECIMAL(12, 4),
    change_percent DECIMAL(8, 4),
    volume_at_snapshot BIGINT,
    bid DECIMAL(12, 4),
    ask DECIMAL(12, 4),
    data_source VARCHAR(50) DEFAULT 'yahoo',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT uq_midday_snapshots_instrument_date UNIQUE (instrument_id, snapshot_date)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_midday_snapshots_instrument_id ON midday_snapshots(instrument_id);
CREATE INDEX IF NOT EXISTS idx_midday_snapshots_date ON midday_snapshots(snapshot_date DESC);
CREATE INDEX IF NOT EXISTS idx_midday_snapshots_instrument_date ON midday_snapshots(instrument_id, snapshot_date DESC);

COMMENT ON TABLE midday_snapshots IS 'Intraday price snapshots captured around 12:00 Sydney time';
COMMENT ON COLUMN midday_snapshots.change_from_open IS 'Price change from market open';
COMMENT ON COLUMN midday_snapshots.change_percent IS 'Percentage change from previous close';
