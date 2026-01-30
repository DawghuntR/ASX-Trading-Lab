---
id: 006
name: Database Schema v1 (Core)
status: Planned
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

- Schema can be applied reproducibly (SQL/migrations) to Supabase Cloud.
- Ingestion can upsert instruments and insert/update daily price records.
- Queries required by the UI are performant for:
  - whole-of-ASX (target)
  - ASX300 fallback
