---
id: 020
name: UI - Symbol Drilldown
status: Planned
---

# 020 - UI: Symbol Drilldown

Provide a per-symbol view showing recent price history, signals, and relevant context.

## Description

- Search/select an ASX symbol.
- Show:
  - recent daily chart (OHLC or close line)
  - latest snapshot
  - recent signals for that symbol
  - recent announcements (once available)

## Impact

- Allows investigation beyond a ranked list.

## Success Criteria

- Symbol page loads from Supabase queries using anon key.
- Chart renders last N days.
- Signals and announcements (if present) are displayed with timestamps.
