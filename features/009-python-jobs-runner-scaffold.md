---
id: 009
name: Python Jobs Runner Scaffold
status: Planned
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

- Provides the “engine room” for daily data refresh and computations.

## Success Criteria

- A single command can run end-to-end locally using env vars.
- Failures are logged clearly and the process exits non-zero on failure.
- Jobs can be rerun idempotently (safe re-run for a given day).
- Runner can be installed and executed headlessly on Ubuntu 24.04.
- Logging works with systemd (stdout/stderr to journald) without needing interactive shells.
