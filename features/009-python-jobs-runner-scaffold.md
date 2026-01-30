---
id: 009
name: Python Jobs Runner Scaffold
status: Completed
completed_date: 2026-01-30
---

# 009 - Python Jobs Runner Scaffold

Create the Python-based jobs runner that performs ingestion and analytics and writes results into Supabase.

## Description

Target runtime: **Ubuntu 24.04.3 LTS** home lab.

- Define Python project structure for:
  - configuration loading
  - logging
  - retries/backoff
  - provider adapters
  - job orchestration (run all daily jobs)
- Implement a single entrypoint command suitable for cron/systemd.

## Impact

- Provides the "engine room" for daily data refresh and computations.

## Success Criteria

- [x] A single command can run end-to-end locally using env vars.
- [x] Failures are logged clearly and the process exits non-zero on failure.
- [x] Jobs can be rerun idempotently (safe re-run for a given day).
- [x] Runner can be installed and executed headlessly on Ubuntu 24.04.
- [x] Logging works with systemd (stdout/stderr to journald) without needing interactive shells.

## Implementation Notes

### Project Structure

```
jobs/
├── pyproject.toml           # Python project config
├── .env.example             # Environment template
└── src/asx_jobs/
    ├── cli.py               # CLI entry point
    ├── config.py            # Configuration management
    ├── database.py          # Supabase client
    ├── logging.py           # Structured logging
    ├── orchestrator.py      # Job orchestration
    ├── providers/
    │   └── yahoo.py         # Yahoo Finance adapter
    └── jobs/
        ├── ingest_symbols.py  # Symbol ingestion
        └── ingest_prices.py   # Price ingestion
```

### Commands

| Command | Description |
|---------|-------------|
| `asx-jobs daily` | Run daily ingestion (symbols + recent prices) |
| `asx-jobs backfill --period 2y` | Backfill historical data |
| `asx-jobs symbols` | Ingest symbols only |

### Features

- Structured JSON logging (systemd compatible)
- Retry with exponential backoff (tenacity)
- Rate limiting for Yahoo Finance API
- Idempotent upsert operations
- Configurable via environment variables

### Setup

See `jobs/README.md` for installation and usage instructions.
