-- Migration: 010_functions
-- Description: Utility functions for common operations
-- Created: 2026-01-30

-- Function: Upsert instrument
CREATE OR REPLACE FUNCTION upsert_instrument(
    p_symbol VARCHAR(10),
    p_name VARCHAR(255) DEFAULT NULL,
    p_sector VARCHAR(100) DEFAULT NULL,
    p_industry VARCHAR(100) DEFAULT NULL,
    p_market_cap BIGINT DEFAULT NULL,
    p_is_asx300 BOOLEAN DEFAULT FALSE,
    p_metadata JSONB DEFAULT '{}'
)
RETURNS BIGINT AS $$
DECLARE
    v_id BIGINT;
BEGIN
    INSERT INTO instruments (symbol, name, sector, industry, market_cap, is_asx300, metadata)
    VALUES (p_symbol, p_name, p_sector, p_industry, p_market_cap, p_is_asx300, p_metadata)
    ON CONFLICT (symbol) DO UPDATE SET
        name = COALESCE(EXCLUDED.name, instruments.name),
        sector = COALESCE(EXCLUDED.sector, instruments.sector),
        industry = COALESCE(EXCLUDED.industry, instruments.industry),
        market_cap = COALESCE(EXCLUDED.market_cap, instruments.market_cap),
        is_asx300 = EXCLUDED.is_asx300,
        metadata = instruments.metadata || EXCLUDED.metadata,
        updated_at = NOW()
    RETURNING id INTO v_id;
    
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Upsert daily price
CREATE OR REPLACE FUNCTION upsert_daily_price(
    p_instrument_id BIGINT,
    p_trade_date DATE,
    p_open DECIMAL(12, 4),
    p_high DECIMAL(12, 4),
    p_low DECIMAL(12, 4),
    p_close DECIMAL(12, 4),
    p_volume BIGINT DEFAULT 0,
    p_adjusted_close DECIMAL(12, 4) DEFAULT NULL,
    p_data_source VARCHAR(50) DEFAULT 'yahoo'
)
RETURNS BIGINT AS $$
DECLARE
    v_id BIGINT;
BEGIN
    INSERT INTO daily_prices (instrument_id, trade_date, open, high, low, close, volume, adjusted_close, data_source)
    VALUES (p_instrument_id, p_trade_date, p_open, p_high, p_low, p_close, p_volume, p_adjusted_close, p_data_source)
    ON CONFLICT (instrument_id, trade_date) DO UPDATE SET
        open = EXCLUDED.open,
        high = EXCLUDED.high,
        low = EXCLUDED.low,
        close = EXCLUDED.close,
        volume = EXCLUDED.volume,
        adjusted_close = COALESCE(EXCLUDED.adjusted_close, daily_prices.adjusted_close),
        data_source = EXCLUDED.data_source
    RETURNING id INTO v_id;
    
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Get price history for symbol
CREATE OR REPLACE FUNCTION get_price_history(
    p_symbol VARCHAR(10),
    p_start_date DATE DEFAULT CURRENT_DATE - INTERVAL '1 year',
    p_end_date DATE DEFAULT CURRENT_DATE
)
RETURNS TABLE (
    trade_date DATE,
    open DECIMAL(12, 4),
    high DECIMAL(12, 4),
    low DECIMAL(12, 4),
    close DECIMAL(12, 4),
    volume BIGINT,
    adjusted_close DECIMAL(12, 4)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        dp.trade_date,
        dp.open,
        dp.high,
        dp.low,
        dp.close,
        dp.volume,
        dp.adjusted_close
    FROM daily_prices dp
    JOIN instruments i ON dp.instrument_id = i.id
    WHERE i.symbol = p_symbol
      AND dp.trade_date BETWEEN p_start_date AND p_end_date
    ORDER BY dp.trade_date ASC;
END;
$$ LANGUAGE plpgsql;

-- Function: Calculate simple moving average
CREATE OR REPLACE FUNCTION calc_sma(
    p_instrument_id BIGINT,
    p_date DATE,
    p_period INTEGER DEFAULT 20
)
RETURNS DECIMAL(12, 4) AS $$
DECLARE
    v_sma DECIMAL(12, 4);
BEGIN
    SELECT AVG(close) INTO v_sma
    FROM (
        SELECT close
        FROM daily_prices
        WHERE instrument_id = p_instrument_id
          AND trade_date <= p_date
        ORDER BY trade_date DESC
        LIMIT p_period
    ) sub;
    
    RETURN v_sma;
END;
$$ LANGUAGE plpgsql;

-- Function: Get ingest status summary
CREATE OR REPLACE FUNCTION get_ingest_status()
RETURNS TABLE (
    total_instruments BIGINT,
    active_instruments BIGINT,
    asx300_instruments BIGINT,
    latest_price_date DATE,
    prices_today BIGINT,
    signals_today BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (SELECT COUNT(*) FROM instruments)::BIGINT,
        (SELECT COUNT(*) FROM instruments WHERE is_active = TRUE)::BIGINT,
        (SELECT COUNT(*) FROM instruments WHERE is_asx300 = TRUE)::BIGINT,
        (SELECT MAX(trade_date) FROM daily_prices),
        (SELECT COUNT(*) FROM daily_prices WHERE trade_date = CURRENT_DATE)::BIGINT,
        (SELECT COUNT(*) FROM signals WHERE signal_date = CURRENT_DATE)::BIGINT;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION upsert_instrument IS 'Insert or update an instrument record';
COMMENT ON FUNCTION upsert_daily_price IS 'Insert or update a daily price record';
COMMENT ON FUNCTION get_price_history IS 'Get price history for a symbol within date range';
COMMENT ON FUNCTION calc_sma IS 'Calculate simple moving average for an instrument';
COMMENT ON FUNCTION get_ingest_status IS 'Get summary of data ingestion status';
