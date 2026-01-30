---
id: 025
name: UI - Backtest Reporting
status: Planned
---

# 025 - UI: Backtest Reporting

Display backtest runs, key metrics, and trades in the GitHub Pages UI.

## Description

- List backtest runs with filters (strategy, universe, date range).
- Show summary metrics (return, drawdown, win rate).
- Show trade log details.

## Impact

- Makes research outputs accessible without running scripts manually.

## Success Criteria

- Backtest results load via Supabase anon key (read-only).
- Metrics and trade log render correctly.
- Basic filtering works.
