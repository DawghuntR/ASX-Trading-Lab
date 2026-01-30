---
id: 006
name: Database Schema v1 (Core)
status: Completed
completed_date: 2026-01-30
---

# 006 - Database Schema v1 (Core)

Define and implement the initial Supabase/Postgres schema that supports daily price ingestion, signals, announcements, backtests, and paper trading.

## Description

Create tables/views (exact names TBD, but must cover):

- Instruments (ASX symbols + metadata)
- Daily OHLCV bars
- Midday snapshot (if stored separately)
- Signals (movement, volatility, etc.)
- Announcements (ASX scraped)
- Backtests (runs, strategies, trades, summary metrics)
- Paper trading ledger (orders/executions) and portfolio snapshots

Include indexes and constraints that support querying by symbol and date.

## Impact

- Provides a stable contract between job runner and frontend.
- Enables RLS/view-based exposure to a public client.

## Success Criteria

- [x] Schema can be applied reproducibly (SQL/migrations) to Supabase Cloud.
- [x] Ingestion can upsert instruments and insert/update daily price records.
- [x] Queries required by the UI are performant for:
  - [x] whole-of-ASX (target)
  - [x] ASX300 fallback

## Implementation Notes

### Tables Created (13 total)

| Table | Purpose |
|-------|---------|
| `instruments` | ASX symbols with metadata |
| `daily_prices` | End-of-day OHLCV data |
| `midday_snapshots` | Intraday price captures |
| `signals` | Trading signals (price movement, volatility, etc.) |
| `announcements` | ASX company announcements |
| `strategies` | Trading strategy definitions |
| `backtest_runs` | Backtest execution runs |
| `backtest_metrics` | Performance metrics per backtest |
| `backtest_trades` | Individual trades in backtests |
| `paper_accounts` | Paper trading accounts |
| `paper_orders` | Paper trading order ledger |
| `paper_positions` | Current paper positions |
| `portfolio_snapshots` | Daily portfolio value history |

### Views (6 total)

- `v_latest_prices` - Latest prices with daily change
- `v_todays_signals` - Current day's signals
- `v_price_movers` - Top gainers/losers
- `v_backtest_leaderboard` - Ranked backtest results
- `v_portfolio_summary` - Paper trading summary
- `v_ingest_health` - Data ingestion status

### Functions

- `upsert_instrument()` - Idempotent instrument upsert
- `upsert_daily_price()` - Idempotent price upsert
- `get_price_history()` - Retrieve price data by symbol
- `calc_sma()` - Calculate simple moving average
- `get_ingest_status()` - Ingestion health summary

### Indexes

Comprehensive indexing strategy for performant queries:
- Symbol lookups: `idx_instruments_symbol`
- Date range queries: `idx_daily_prices_instrument_date`
- Covering index for OHLCV: `idx_daily_prices_date_range`
- Signal queries: `idx_signals_type_date`, `idx_signals_strength`
- Full-text search: `idx_announcements_headline_fts`

### RLS Policies

All tables have public read-only access via `anon` role. Service role has full access for job runner operations.

### Setup

See `database/README.md` for migration instructions.
