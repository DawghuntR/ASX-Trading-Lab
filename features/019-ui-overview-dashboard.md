---
id: 019
name: UI - Overview Dashboard
status: Planned
---

# 019 - UI: Overview Dashboard

Provide a landing dashboard in the GitHub Pages app showing ingest health and the most important daily outputs.

## Description

- Show last successful ingest run, coverage, and staleness.
- Show top signals for the day:
  - price movement
  - volatility spikes
- Provide links into symbol drilldown.

## Impact

- Turns raw ingestion into a usable daily workflow.

## Success Criteria

- Loads quickly from GitHub Pages.
- Displays ingest health sourced from Supabase.
- Displays a ranked list of today’s signals.
