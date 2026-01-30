---
id: 024
name: Strategy Pack v1
status: Planned
---

# 024 - Strategy Pack v1

Define and ship an initial set of simple strategies to validate the backtesting engine and build intuition.

## Description

Include at least two strategies based on your original examples, implemented in a consistent format:

- Mean reversion example:
  - Buy if a stock drops 3 days in a row
  - Sell after a 2% bounce (or after N days)
- Breakout example:
  - Buy breakouts above a 20-day high
  - Exit rule (define: stop, trailing, time-based)

## Impact

- Provides immediate “known test cases” and reduces blank-page risk.

## Success Criteria

- Strategies run without errors in Backtesting Engine v1.
- Each strategy has documented parameters and assumptions.
- Outputs include trade logs and summary metrics.
