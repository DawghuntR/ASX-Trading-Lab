---
id: 007
name: Public Read-Only Access (RLS + Views)
status: Planned
---

# 007 - Public Read-Only Access (RLS + Views)

Allow the GitHub Pages client to read data from Supabase safely using the anon key while preventing public writes.

## Description

- Enable Row Level Security (RLS) on relevant tables.
- Expose only the minimum necessary read surfaces to the public client, preferably via:
  - read-only views
  - whitelisted columns
- Ensure writes are restricted to the jobs runner (service role).

## Impact

- Makes “public dashboard” possible without authentication.
- Reduces risk of vandalism or unintended data mutation.

## Success Criteria

- GitHub Pages client can query required datasets (signals, OHLCV, announcements, backtests summaries).
- Public client cannot insert/update/delete on protected tables.
- Service role can perform ingestion writes.
