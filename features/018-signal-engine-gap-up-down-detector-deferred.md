---
id: 018
name: Signal Engine - Gap Up/Down Detector (Deferred)
status: Planned
---

# 018 - Signal Engine: Gap Up/Down Detector (Deferred)

Detect gap up/down events at market open and track gap-fill behavior.

## Description

This module is currently **deferred** because the v1 platform runs once daily at midday Sydney time and does not capture market-open data.

When enabled, it will:

- Compare yesterday close vs today open.
- Flag gaps > threshold (e.g., ±3%).
- Track whether the gap fills during the day.

## Impact

- Adds a classic short-term signal for mean reversion study.

## Success Criteria

- When an open-time dataset is available, gaps are computed and persisted.
- UI can show today’s gaps and subsequent gap-fill outcome.
