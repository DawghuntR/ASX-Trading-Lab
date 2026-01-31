# Restores

Clear steps for recovering databases safely.

---

## Use Supabase Cloud

Run a point-in-time restore from the Supabase dashboard.
Open Project settings → Database → Backups and choose the restore time.

### Get help

If you need a full project restore, contact Supabase support.
Share the project ref, desired timestamp, and incident details.

---

## Restore self-hosted PostgreSQL (Ubuntu 24.04)

Stop writers before you restore and verify the backup file.
Keep a copy of the backup in a separate location.

### Checklist

- Stop job runners and API services
- Verify the backup file checksum or size
- Confirm target database name and credentials

### Restore with pg_restore

Use this when the backup is in custom format.

```bash
sudo -u postgres pg_restore --clean --if-exists --dbname=asx_trading_lab \
  "/var/backups/asx-trading-lab/asx-trading-lab-2026-01-31-0230.sql.gz"
```

### Restore with psql

Use this when the backup is plain SQL.

```bash
sudo -u postgres psql --dbname=asx_trading_lab \
  --file "/var/backups/asx-trading-lab/asx-trading-lab-2026-01-31-0230.sql"
```

### Verify after restore

```bash
sudo -u postgres psql --dbname=asx_trading_lab -c "select count(*) from job_runs"
sudo -u postgres psql --dbname=asx_trading_lab -c "select max(created_at) from signals"
```

### Restart services

```bash
sudo systemctl start asx-jobs
sudo systemctl start asx-api
```

---

## Handle partial restores

Restore a single table when you only need specific data.
Use a temporary database to validate the data first.

### Restore one table

```bash
sudo -u postgres pg_restore --dbname=asx_trading_lab \
  --table=signals \
  "/var/backups/asx-trading-lab/asx-trading-lab-2026-01-31-0230.sql.gz"
```

### Restore to a test database

```bash
sudo -u postgres createdb asx_trading_lab_restore_test
sudo -u postgres pg_restore --dbname=asx_trading_lab_restore_test \
  "/var/backups/asx-trading-lab/asx-trading-lab-2026-01-31-0230.sql.gz"
```

Tip: compare row counts before switching production back.

---

## Related docs

- [Backup procedures](backup-procedures.md)
- [Data retention policies](data-retention.md)
