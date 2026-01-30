-- Migration: 005_announcements
-- Description: ASX company announcements scraped from ASX website
-- Created: 2026-01-30

-- Announcement sensitivity enum
CREATE TYPE announcement_sensitivity AS ENUM (
    'price_sensitive',
    'not_price_sensitive',
    'unknown'
);

CREATE TABLE IF NOT EXISTS announcements (
    id BIGSERIAL PRIMARY KEY,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    announced_at TIMESTAMPTZ NOT NULL,
    headline TEXT NOT NULL,
    url TEXT,
    document_type VARCHAR(100),
    sensitivity announcement_sensitivity DEFAULT 'unknown',
    pages INTEGER,
    file_size_kb INTEGER,
    asx_announcement_id VARCHAR(50),
    content_hash VARCHAR(64),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT uq_announcements_asx_id UNIQUE (asx_announcement_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_announcements_instrument_id ON announcements(instrument_id);
CREATE INDEX IF NOT EXISTS idx_announcements_date ON announcements(announced_at DESC);
CREATE INDEX IF NOT EXISTS idx_announcements_instrument_date ON announcements(instrument_id, announced_at DESC);
CREATE INDEX IF NOT EXISTS idx_announcements_sensitivity ON announcements(sensitivity) 
    WHERE sensitivity = 'price_sensitive';

-- Full-text search on headline
CREATE INDEX IF NOT EXISTS idx_announcements_headline_fts 
    ON announcements USING GIN (to_tsvector('english', headline));

COMMENT ON TABLE announcements IS 'ASX company announcements scraped from ASX website';
COMMENT ON COLUMN announcements.sensitivity IS 'Whether announcement is marked price sensitive by ASX';
COMMENT ON COLUMN announcements.content_hash IS 'SHA-256 hash for deduplication';
