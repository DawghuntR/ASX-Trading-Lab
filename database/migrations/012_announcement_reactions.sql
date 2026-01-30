-- Migration: 012_announcement_reactions
-- Description: Store computed 1-day price reactions for announcements
-- Feature: 022 - News Reaction Analytics (1D)
-- Created: 2026-01-31

CREATE TABLE IF NOT EXISTS announcement_reactions (
    id BIGSERIAL PRIMARY KEY,
    announcement_id BIGINT NOT NULL REFERENCES announcements(id) ON DELETE CASCADE,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    announcement_date DATE NOT NULL,
    
    -- Price data on announcement day
    announcement_close DECIMAL(12, 4),
    announcement_volume BIGINT,
    
    -- Next trading day price data (1D reaction)
    next_day_date DATE,
    next_day_open DECIMAL(12, 4),
    next_day_close DECIMAL(12, 4),
    next_day_high DECIMAL(12, 4),
    next_day_low DECIMAL(12, 4),
    next_day_volume BIGINT,
    
    -- Computed reaction metrics
    return_1d DECIMAL(8, 4),
    return_1d_pct DECIMAL(8, 4),
    gap_open_pct DECIMAL(8, 4),
    intraday_range_pct DECIMAL(8, 4),
    volume_change_pct DECIMAL(8, 4),
    
    -- Classification
    reaction_direction VARCHAR(10) CHECK (reaction_direction IN ('positive', 'negative', 'neutral')),
    reaction_strength VARCHAR(10) CHECK (reaction_strength IN ('weak', 'medium', 'strong')),
    
    -- Announcement metadata (denormalized for efficient querying)
    document_type VARCHAR(100),
    sensitivity VARCHAR(20),
    headline TEXT,
    
    -- Timestamps
    computed_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT uq_announcement_reaction UNIQUE (announcement_id)
);

-- Indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_reactions_instrument_id ON announcement_reactions(instrument_id);
CREATE INDEX IF NOT EXISTS idx_reactions_date ON announcement_reactions(announcement_date DESC);
CREATE INDEX IF NOT EXISTS idx_reactions_document_type ON announcement_reactions(document_type);
CREATE INDEX IF NOT EXISTS idx_reactions_sensitivity ON announcement_reactions(sensitivity);
CREATE INDEX IF NOT EXISTS idx_reactions_direction ON announcement_reactions(reaction_direction);
CREATE INDEX IF NOT EXISTS idx_reactions_strength ON announcement_reactions(reaction_strength);

-- Composite index for aggregation queries
CREATE INDEX IF NOT EXISTS idx_reactions_type_direction 
    ON announcement_reactions(document_type, reaction_direction);
CREATE INDEX IF NOT EXISTS idx_reactions_sensitivity_direction 
    ON announcement_reactions(sensitivity, reaction_direction);

-- Comments
COMMENT ON TABLE announcement_reactions IS 'Computed 1-day price reactions following ASX announcements';
COMMENT ON COLUMN announcement_reactions.return_1d IS 'Absolute return: next_day_close - announcement_close';
COMMENT ON COLUMN announcement_reactions.return_1d_pct IS 'Percentage return: (next_day_close - announcement_close) / announcement_close * 100';
COMMENT ON COLUMN announcement_reactions.gap_open_pct IS 'Overnight gap: (next_day_open - announcement_close) / announcement_close * 100';
COMMENT ON COLUMN announcement_reactions.intraday_range_pct IS 'Next day range: (high - low) / open * 100';
COMMENT ON COLUMN announcement_reactions.volume_change_pct IS 'Volume change: (next_day_volume - announcement_volume) / announcement_volume * 100';
