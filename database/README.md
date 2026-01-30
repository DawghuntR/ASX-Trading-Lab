# Schema guide
Fast orientation to tables, flows, and access.

---

## Overview
This schema powers ASX instruments, market data, signals, announcements, backtests, and paper trading.
It is designed for append-heavy price data and read-optimized analytics.

---

## Describe tables
- **instruments**: Master list of ASX symbols with metadata and status flags.
- **daily_prices**: End-of-day OHLCV history keyed by instrument and trade date.
- **midday_snapshots**: Mid-session price snapshot per instrument per day.
- **signals**: Generated alerts with type, direction, and optional strength.
- **announcements**: ASX releases with headline, sensitivity, and metadata.
- **strategies**: Backtest strategy definitions and parameters.
- **backtest_runs**: Execution records for a strategy over a date range.
- **backtest_metrics**: One-row summary metrics per backtest run.
- **backtest_trades**: Trade-level outcomes linked to runs and instruments.
- **paper_accounts**: Simulated accounts with balances and status.
- **paper_orders**: Order ledger for paper trading.
- **paper_positions**: Current holdings per account and instrument.
- **portfolio_snapshots**: Daily portfolio value snapshots per account.

---

## Apply migrations
Use the Supabase SQL Editor and paste the migrations in order.
`database/migrations/000_run_all.sql` includes the sequence and notes.

**Steps**
1. Open Supabase Dashboard → SQL Editor → New query.
2. Paste the full contents of each migration file in order, or paste the master script and replace the placeholder with each file’s contents.
3. Run the query and confirm the tables, views, and functions appear.

**Tip**
Keep a single SQL Editor tab for migrations so the order stays consistent.

---

## Map relationships
- `daily_prices`, `midday_snapshots`, `signals`, and `announcements` each reference `instruments`.
- `backtest_runs` belongs to `strategies`, while `backtest_metrics` is one-to-one with `backtest_runs`.
- `backtest_trades` links `backtest_runs` to `instruments` for trade-level history.
- `paper_orders`, `paper_positions`, and `portfolio_snapshots` belong to `paper_accounts` and reference `instruments` where needed.

---

## Review indexes
- `instruments(symbol)` for fast symbol lookup and upserts.
- `daily_prices(instrument_id, trade_date DESC)` for price history and latest close queries.
- `midday_snapshots(instrument_id, snapshot_date DESC)` for intraday retrieval by symbol.
- `signals(signal_type, signal_date DESC)` for dashboards by signal type.
- `announcements` has a GIN index on headline for full-text search.
- `backtest_runs(status)` to filter current and completed runs.
- `paper_orders(status, submitted_at DESC)` for order tracking queues.
- `portfolio_snapshots(account_id, snapshot_date DESC)` for account performance charts.

---

## Explain access
RLS is enabled for all tables with anonymous read-only policies.
The `service_role` bypasses RLS for trusted ingestion and job runners.

---

## List views and functions
**Views**
- `v_latest_prices`: Latest daily price per instrument with percent change.
- `v_todays_signals`: Signals for the current date with instrument context.
- `v_price_movers`: Top gainers and losers for the latest trade date.
- `v_backtest_leaderboard`: Ranked backtest runs by Sharpe ratio.
- `v_portfolio_summary`: Active paper accounts with total value and returns.
- `v_ingest_health`: Quick ingest coverage and freshness snapshot.

**Functions**
- `upsert_instrument`: Insert or update instrument details by symbol.
- `upsert_daily_price`: Insert or update daily OHLCV for a date.
- `get_price_history`: Fetch price history for a symbol and range.
- `calc_sma`: Compute simple moving average for a date and period.
- `get_ingest_status`: Summary counts for ingestion health checks.

---

## Set up environment
- Ensure your Supabase project has the `service_role` key stored outside source control.
- Use a separate ingestion key for jobs and keep anon key for read-only clients.
- Time-series loaders should run in UTC and store `trade_date` in local market date.

**Note**
Metadata fields are JSONB, so you can extend without schema changes.

---

## Explore related docs
- Main project README: [`../README.md`](../README.md)
- Migrations folder: [`./migrations`](./migrations)
