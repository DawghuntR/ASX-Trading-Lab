# Retention

Practical guidelines for keeping data lean and useful.

---

## Define windows

Use the table below to align cleanup with product needs.
Adjust periods only with stakeholder approval.

| Data Type | Retention Period | Rationale |
|-----------|------------------|-----------|
| OHLCV price history | Indefinite (5+ years) | Required for backtesting |
| Announcements | Indefinite | Historical research value |
| Signals | 2 years rolling | UI displays recent, old signals less useful |
| Job run logs | 90 days | Operational troubleshooting |
| Data quality issues | 90 days (resolved), 1 year (unresolved) | Audit trail |
| Backtest runs & trades | 1 year | Keep recent analysis |
| Paper trading history | 1 year | Performance tracking |
| Portfolio snapshots | 1 year | Performance tracking |

---

## Implement cleanup

Use SQL scripts for predictable cleanup runs.
Schedule cleanup with systemd or run on demand.

### Run manually

```bash
psql "$ASX_DATABASE_URL" -f /opt/asx-trading-lab/retention-cleanup.sql
```

### Schedule with systemd

```ini
[Unit]
Description=ASX Trading Lab retention cleanup

[Service]
Type=oneshot
User=postgres
Group=postgres
ExecStart=/usr/bin/psql "$ASX_DATABASE_URL" -f /opt/asx-trading-lab/retention-cleanup.sql
EnvironmentFile=/etc/asx-trading-lab/db.env
```

```ini
[Unit]
Description=Run ASX Trading Lab retention cleanup weekly

[Timer]
OnCalendar=Sun *-*-* 03:15:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now asx-retention.timer
systemctl list-timers --all | grep asx-retention
```

---

## Verify results

Check counts before and after cleanup.
Record results in your ops log.

```bash
psql "$ASX_DATABASE_URL" -c "select count(*) from job_runs"
psql "$ASX_DATABASE_URL" -c "select count(*) from signals"
```

---

## Archive or delete

Archive if records are needed for audits or analytics.
Delete only after exporting data and confirming restore paths.

Tip: export tables to a dated CSV or pg_dump file before deletion.

---

## Related docs

- [Backup procedures](backup-procedures.md)
- [Restore procedures](restore-procedures.md)
