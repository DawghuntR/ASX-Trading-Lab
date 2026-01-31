---
id: 038
name: Performance & Rate-Limit Management
status: Completed
---

# 038 - Performance & Rate-Limit Management

Ensure the daily ingestion and UI queries remain performant, especially for whole-of-ASX coverage using free endpoints.

## Description

- Define provider-side throttling and batching rules.
- Add caching and incremental updates.
- Add DB indexes/materialized views if needed for fast dashboard queries.
- Define acceptable runtime budgets for daily jobs.

## Impact

- Keeps the system usable and stable on home-lab resources.

## Success Criteria

- Daily ingestion completes within a documented time budget for ASX300 fallback.
- UI queries for dashboards return within a documented target.
- Provider calls respect throttling rules.
