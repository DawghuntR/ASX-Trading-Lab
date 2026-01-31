-- Migration: 013_provider_mappings
-- Description: Provider-specific symbol mappings for data normalization
-- Created: 2026-01-31

-- Provider mappings table for translating canonical symbols to provider-specific formats
CREATE TABLE IF NOT EXISTS provider_mappings (
    id BIGSERIAL PRIMARY KEY,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL,
    provider_symbol VARCHAR(50) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    CONSTRAINT uq_provider_instrument UNIQUE (instrument_id, provider),
    CONSTRAINT uq_provider_symbol UNIQUE (provider, provider_symbol)
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_provider_mappings_instrument ON provider_mappings(instrument_id);
CREATE INDEX IF NOT EXISTS idx_provider_mappings_provider ON provider_mappings(provider);
CREATE INDEX IF NOT EXISTS idx_provider_mappings_provider_symbol ON provider_mappings(provider, provider_symbol);
CREATE INDEX IF NOT EXISTS idx_provider_mappings_active ON provider_mappings(is_active) WHERE is_active = TRUE;

-- Trigger to auto-update updated_at
CREATE TRIGGER provider_mappings_updated_at
    BEFORE UPDATE ON provider_mappings
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Symbol history table for tracking renames and corporate actions
CREATE TABLE IF NOT EXISTS symbol_history (
    id BIGSERIAL PRIMARY KEY,
    instrument_id BIGINT NOT NULL REFERENCES instruments(id) ON DELETE CASCADE,
    old_symbol VARCHAR(10) NOT NULL,
    new_symbol VARCHAR(10) NOT NULL,
    change_type VARCHAR(50) NOT NULL,
    effective_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for symbol history
CREATE INDEX IF NOT EXISTS idx_symbol_history_instrument ON symbol_history(instrument_id);
CREATE INDEX IF NOT EXISTS idx_symbol_history_old_symbol ON symbol_history(old_symbol);
CREATE INDEX IF NOT EXISTS idx_symbol_history_effective_date ON symbol_history(effective_date);

-- Enable RLS on new tables
ALTER TABLE provider_mappings ENABLE ROW LEVEL SECURITY;
ALTER TABLE symbol_history ENABLE ROW LEVEL SECURITY;

-- Public read-only policies
CREATE POLICY "Public read access for provider_mappings"
    ON provider_mappings FOR SELECT
    TO anon
    USING (true);

CREATE POLICY "Public read access for symbol_history"
    ON symbol_history FOR SELECT
    TO anon
    USING (true);

-- Function to get provider symbol from canonical symbol
CREATE OR REPLACE FUNCTION get_provider_symbol(
    p_symbol VARCHAR,
    p_provider VARCHAR DEFAULT 'yahoo'
) RETURNS VARCHAR AS $$
DECLARE
    v_provider_symbol VARCHAR;
BEGIN
    SELECT pm.provider_symbol INTO v_provider_symbol
    FROM provider_mappings pm
    JOIN instruments i ON i.id = pm.instrument_id
    WHERE i.symbol = p_symbol 
      AND pm.provider = p_provider
      AND pm.is_active = TRUE;
    
    IF v_provider_symbol IS NULL THEN
        -- Default fallback: append provider suffix
        IF p_provider = 'yahoo' THEN
            RETURN p_symbol || '.AX';
        ELSE
            RETURN p_symbol;
        END IF;
    END IF;
    
    RETURN v_provider_symbol;
END;
$$ LANGUAGE plpgsql STABLE;

-- Function to get canonical symbol from provider symbol
CREATE OR REPLACE FUNCTION get_canonical_symbol(
    p_provider_symbol VARCHAR,
    p_provider VARCHAR DEFAULT 'yahoo'
) RETURNS VARCHAR AS $$
DECLARE
    v_symbol VARCHAR;
BEGIN
    SELECT i.symbol INTO v_symbol
    FROM provider_mappings pm
    JOIN instruments i ON i.id = pm.instrument_id
    WHERE pm.provider_symbol = p_provider_symbol 
      AND pm.provider = p_provider
      AND pm.is_active = TRUE;
    
    IF v_symbol IS NULL THEN
        -- Default fallback: strip provider suffix
        IF p_provider = 'yahoo' AND p_provider_symbol LIKE '%.AX' THEN
            RETURN LEFT(p_provider_symbol, LENGTH(p_provider_symbol) - 3);
        ELSE
            RETURN p_provider_symbol;
        END IF;
    END IF;
    
    RETURN v_symbol;
END;
$$ LANGUAGE plpgsql STABLE;

-- View for easy provider mapping lookup
CREATE OR REPLACE VIEW v_provider_mappings AS
SELECT 
    i.id AS instrument_id,
    i.symbol AS canonical_symbol,
    i.name AS instrument_name,
    pm.provider,
    pm.provider_symbol,
    pm.is_active,
    pm.notes
FROM instruments i
LEFT JOIN provider_mappings pm ON i.id = pm.instrument_id
WHERE i.is_active = TRUE;

-- Comments
COMMENT ON TABLE provider_mappings IS 'Maps canonical ASX symbols to provider-specific ticker formats';
COMMENT ON COLUMN provider_mappings.provider IS 'Data provider identifier (yahoo, asx, etc.)';
COMMENT ON COLUMN provider_mappings.provider_symbol IS 'Provider-specific symbol format (e.g., BHP.AX for Yahoo)';

COMMENT ON TABLE symbol_history IS 'Tracks symbol changes from corporate actions and renames';
COMMENT ON COLUMN symbol_history.change_type IS 'Type of change: rename, merger, demerger, delisting, etc.';

COMMENT ON FUNCTION get_provider_symbol IS 'Converts canonical ASX symbol to provider-specific format';
COMMENT ON FUNCTION get_canonical_symbol IS 'Converts provider-specific symbol back to canonical ASX format';
