---
id: 023
name: Backtesting Engine v1
status: Planned
---

# 023 - Backtesting Engine v1

Implement a simple historical backtesting engine using daily bars to simulate rule-based strategies.

## Description

- Use ingested historical daily bars.
- Simulate trades based on strategy rules.
- Persist:
  - backtest run metadata
  - trades
  - summary metrics (win rate, total return, max drawdown)

## Impact

- Moves development from “signals” to validated, data-driven strategy iteration.

## Success Criteria

- Can run at least two strategies end-to-end.
- Produces stored metrics and trade logs.
- Results are reproducible for a fixed date range and universe.
