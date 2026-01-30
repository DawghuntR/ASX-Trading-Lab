---
id: 026
name: Paper Trading Ledger v1 (EOD)
status: Planned
---

# 026 - Paper Trading Ledger v1 (EOD)

Implement paper trading as a persisted ledger of simulated executions using end-of-day (daily close) fills.

## Description

- Consume signals (or manual triggers) and record simulated trades.
- Use daily close as fill price (v1).
- Persist orders/executions and positions.

## Impact

- Enables forward-testing strategies without real money.

## Success Criteria

- Paper trades can be recorded deterministically for a given day.
- Positions and basic P/L can be derived from the ledger.
- Data is queryable by the UI.
