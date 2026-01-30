---
id: 025
name: UI - Backtest Reporting
status: Completed
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

## Implementation

### Files Created/Modified

- `frontend/src/hooks/useData.ts` - Added `useBacktestRuns`, `useBacktestDetail`, `useStrategies` hooks
- `frontend/src/pages/BacktestsPage.tsx` - Updated with live data, filters, stats summary, and runs table
- `frontend/src/pages/BacktestsPage.module.css` - Updated with comprehensive styles
- `frontend/src/pages/BacktestDetailPage.tsx` - New page with metrics, equity curve, and trade log
- `frontend/src/pages/BacktestDetailPage.module.css` - New styles for detail page
- `frontend/src/App.tsx` - Added `/backtests/:id` route

### Features

1. **Backtests List Page** (`/backtests`)
   - Summary stats (total runs, completed, avg return, strategies count)
   - Filter by strategy and status
   - Table with ID, strategy, name, period, capital, return, status
   - Links to detail page

2. **Backtest Detail Page** (`/backtests/:id`)
   - Run summary (initial/final capital, total return, total trades)
   - Full performance metrics grid (14 metrics including Sharpe, Sortino, drawdown, win rate, etc.)
   - SVG equity curve visualization
   - Complete trade log table with symbol links, entry/exit details, P&L
