# Backups

Step-by-step options for protecting ASX Trading Lab data.

---

## Confirm scope

Back up the database, environment files, and configuration files.
Store .env files outside git, with restricted access.

---

## Use Supabase Cloud

Supabase Cloud includes automatic point-in-time recovery (PITR).
Open the Supabase dashboard and go to Project settings → Database → Backups.

### Export manually

Use pg_dump via the Supabase CLI for an on-demand snapshot.

```bash
supabase login
supabase link --project-ref <project-ref>
supabase db dump --db-url "postgresql://<user>:<password>@<host>:<port>/<db>" --file "asx-trading-lab-$(date +%F).sql"
```

Tip: store exports in a restricted backup bucket or encrypted volume.

---

## Back up self-hosted PostgreSQL (Ubuntu 24.04)

Use pg_dump for routine logical backups.
Save backups under `/var/backups/asx-trading-lab/` with timestamped filenames.

### Create a backup script

```bash
sudo install -d -m 0750 -o postgres -g postgres /var/backups/asx-trading-lab
sudo tee /usr/local/bin/asx-db-backup >/dev/null <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="/var/backups/asx-trading-lab"
STAMP="$(date +%F-%H%M)"
FILE="$BACKUP_DIR/asx-trading-lab-$STAMP.sql.gz"

pg_dump --format=custom --file="$FILE" "$ASX_DATABASE_URL"
EOF
sudo chmod 0750 /usr/local/bin/asx-db-backup
sudo chown postgres:postgres /usr/local/bin/asx-db-backup
```

Note: set `ASX_DATABASE_URL` in a root- or postgres-owned environment file.

### Run and verify

```bash
sudo -u postgres /usr/local/bin/asx-db-backup
ls -lh /var/backups/asx-trading-lab
```

---

## Schedule with systemd (optional)

Use a timer to run nightly backups.
Save units under `/etc/systemd/system/`.

### Service unit

```ini
[Unit]
Description=ASX Trading Lab database backup

[Service]
Type=oneshot
User=postgres
Group=postgres
ExecStart=/usr/local/bin/asx-db-backup
EnvironmentFile=/etc/asx-trading-lab/db.env
```

### Timer unit

```ini
[Unit]
Description=Run ASX Trading Lab database backup nightly

[Timer]
OnCalendar=*-*-* 02:30:00
Persistent=true

[Install]
WantedBy=timers.target
```

### Enable and check

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now asx-db-backup.timer
systemctl list-timers --all | grep asx-db-backup
```

---

## Protect env and config files

Keep .env files in a restricted directory, backed up separately.
Include service config and job scheduler units if you use them.

Suggested locations:

- `/etc/asx-trading-lab/`
- `/etc/systemd/system/`
- `/var/backups/asx-trading-lab/`

---

## Related docs

- [Restore procedures](restore-procedures.md)
- [Data retention policies](data-retention.md)
