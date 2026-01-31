---
id: 037
name: Backups, Restore, and Data Retention
status: Completed
---

# 037 - Backups, Restore, and Data Retention

Define backup/restore procedures and retention policies for the Supabase database (cloud and self-host modes).

## Description

- Decide retention policies for:
  - OHLCV history
  - announcements
  - job run logs
  - backtests
  - paper trading history
- Provide restore instructions.
- For self-host mode, document volume backups.
- For Ubuntu deployments, document:
  - backup storage location expectations
  - permissions/ownership considerations
  - any systemd timer option for scheduled backups (if desired)

## Impact

- Prevents catastrophic data loss and supports long-term research.

## Success Criteria

- Backup procedure is documented and test-restored at least once.
- Retention rules are documented and implementable.
