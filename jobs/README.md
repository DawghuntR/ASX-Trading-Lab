# Jobs runner
Python CLI for ASX ingestion workflows.

---
## Understand
Runs daily, backfill, and symbol ingestion tasks for ASX Trading Lab. Includes Feature 009 scaffold, Feature 011 symbol universe ingestion, and Feature 012 Yahoo Finance adapter.

---
## Prepare
Requires Python 3.11+ and pip. A Supabase project is also required for storage.

---
## Install
From the `jobs/` directory:

```bash
pip install -e .
```

---
## Configure
Create a `.env` file in `jobs/` with the required keys.

Use the template:

```bash
cp .env.example .env
```

```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
```

Tip: You can pass a custom path via `--env-file`.

---
## Run
Daily ingestion:

```bash
asx-jobs daily
```

Backfill historical prices:

```bash
asx-jobs backfill --period 2y
```

Symbols only (with metadata):

```bash
asx-jobs symbols
```

Symbols only (no metadata):

```bash
asx-jobs symbols --no-metadata
```

---
## Paper trading

Paper trading is implemented as an end-of-day (EOD) ledger and can be operated via CLI.

Create an account:

```bash
asx-jobs paper account create "My Account" --balance 100000
asx-jobs paper account list
asx-jobs paper account show 1
```

Submit orders (filled at EOD close in v1; limit orders use day high/low eligibility):

```bash
asx-jobs paper order buy BHP 100 --account 1
asx-jobs paper order sell CBA 50 --account 1 --limit 95.00
asx-jobs paper order list --account 1
```

Execute and snapshot:

```bash
asx-jobs paper execute --date 2026-01-30
asx-jobs paper snapshot --account 1 --date 2026-01-30
```

Performance and risk reports:

```bash
asx-jobs paper metrics --account 1
asx-jobs paper risk --account 1
```

Related features:

- Feature **026** (paper ledger)
- Feature **027** (portfolio performance metrics)
- Feature **028** (risk rules & metrics)


---
## Explore
Key paths in this package:

- `src/asx_jobs/cli.py` — command entry point
- `src/asx_jobs/orchestrator.py` — job coordination
- `src/asx_jobs/jobs/` — job implementations
- `src/asx_jobs/providers/` — data providers (Yahoo)
- `src/asx_jobs/config.py` — configuration loader

---
## Schedule
Example systemd service and timer files.

`/etc/systemd/system/asx-jobs.service`:

```ini
[Unit]
Description=ASX Jobs Runner
After=network.target

[Service]
Type=oneshot
WorkingDirectory=/home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs
EnvironmentFile=/home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs/.env
ExecStart=/usr/bin/asx-jobs daily
```

`/etc/systemd/system/asx-jobs.timer`:

```ini
[Unit]
Description=Run ASX Jobs daily

[Timer]
OnCalendar=Mon..Fri 18:00
Persistent=true

[Install]
WantedBy=timers.target
```

Cron example (weekdays at 6pm):

```cron
0 18 * * 1-5 cd /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs && /usr/bin/asx-jobs daily
```

Note: Keep the `.env` readable by the service user.

---
## Develop
Create a virtual environment and install dev dependencies.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Lint and type-check:

```bash
ruff check .
mypy src
```

---
## See also
- [Project overview](../README.md)
