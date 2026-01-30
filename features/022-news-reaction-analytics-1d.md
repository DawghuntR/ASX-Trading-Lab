---
id: 022
name: News Reaction Analytics (1D)
status: Completed
---

# 022 - News Reaction Analytics (1D)

Measure and store the typical 1-day price reaction following ASX announcements.

## Description

- For each ingested announcement, compute next-day reaction metrics using daily bars:
  - 1-day return after announcement date (define exact alignment rules)
- Produce aggregated summaries by announcement category (if available) or keyword rules.

## Impact

- Builds empirical “news impact” intuition from your own dataset.

## Success Criteria

- Per-announcement 1D reaction metric is computed and stored.
- At least one aggregated view/report can be produced (e.g., by keyword/category).
- Results are viewable in the UI.
