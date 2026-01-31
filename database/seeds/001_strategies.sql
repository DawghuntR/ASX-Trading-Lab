-- Seed: 001_strategies
-- Description: Initial trading strategies for backtesting
-- Created: 2026-01-31
--
-- Run this in your Supabase SQL Editor or via psql:
--   psql $DATABASE_URL -f database/seeds/001_strategies.sql

-- Strategy 1: Mean Reversion
-- Buys after consecutive down days, exits on profit target or time stop
INSERT INTO strategies (name, description, version, parameters, is_active)
VALUES (
    'Mean Reversion',
    'Buy after 3 consecutive down days with >3% total drop. Exit at 2% profit, 5% stop loss, or 10 day time limit.',
    '1.0.0',
    '{
        "consecutive_down_days": 3,
        "target_bounce_pct": 2.0,
        "max_holding_days": 10,
        "stop_loss_pct": 5.0,
        "min_drop_pct": 3.0,
        "min_price": 0.10,
        "min_volume": 100000
    }'::jsonb,
    TRUE
)
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    version = EXCLUDED.version,
    parameters = EXCLUDED.parameters,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

-- Strategy 2: Breakout
-- Buys on 20-day high breakout with volume confirmation, exits via trailing stop
INSERT INTO strategies (name, description, version, parameters, is_active)
VALUES (
    'Breakout',
    'Buy when price breaks 1%+ above 20-day high with 1.5x volume. Exit with 5% trailing stop, 3% initial stop, or 20 day limit.',
    '1.0.0',
    '{
        "lookback_days": 20,
        "trailing_stop_pct": 5.0,
        "stop_loss_pct": 3.0,
        "max_holding_days": 20,
        "min_breakout_pct": 1.0,
        "require_volume_confirmation": true,
        "volume_multiplier": 1.5,
        "min_price": 0.50
    }'::jsonb,
    TRUE
)
ON CONFLICT (name) DO UPDATE SET
    description = EXCLUDED.description,
    version = EXCLUDED.version,
    parameters = EXCLUDED.parameters,
    is_active = EXCLUDED.is_active,
    updated_at = NOW();

-- Verify insertion
SELECT id, name, version, is_active, created_at 
FROM strategies 
ORDER BY id;
