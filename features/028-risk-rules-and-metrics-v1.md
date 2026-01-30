---
id: 028
name: Risk Rules & Metrics v1
status: Planned
---

# 028 - Risk Rules & Metrics v1

Implement risk tracking rules and metrics to prevent over-exposure and to monitor drawdowns.

## Description

- Track:
  - total exposure
  - position concentration (% per symbol)
  - losing streaks
  - drawdown thresholds
- Define initial risk limits (configurable).

## Impact

- Acts as a discipline layer for paper trading and future live considerations.

## Success Criteria

- Risk metrics can be computed from paper portfolio state.
- Rule violations can be detected deterministically.
- Outputs are queryable for UI display.
