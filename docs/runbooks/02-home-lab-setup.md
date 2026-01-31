# Home lab
Run the jobs runner on Ubuntu 24.04.

---

## Confirm prerequisites
- Ubuntu 24.04 LTS host.
- Python 3.11+ and git installed.
- Supabase project URL and service role key.

Verification:
```bash
lsb_release -a
python3 --version
git --version
```

---

## Clone the repo
```bash
git clone https://github.com/<you>/ASX-Trading-Lab.git
cd ASX-Trading-Lab
```

Verification:
```bash
git status
```

---

## Create a virtual environment
```bash
cd /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs
python3 -m venv .venv
source .venv/bin/activate
```

Verification:
```bash
which python
```

---

## Install the runner
```bash
pip install -e .
```

Verification:
```bash
asx-jobs --help
```

Related: [Jobs runner](../../jobs/README.md)

---

## Configure environment
```bash
cp .env.example .env
```

Edit `jobs/.env` with these values:
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

Verification:
```bash
source .env
echo "$SUPABASE_URL"
```

Related: [Feature 008](../../features/008-configuration-and-secrets-management.md)

---

## Install systemd units
```bash
cd /home/dawghuntr/gitRepos/ASX-Trading-Lab/deploy
sudo ./install.sh
```

Verification:
```bash
systemctl status asx-jobs.timer
```

Related: [Deploy guide](../../deploy/README.md)

---

## Enable and start the timer
```bash
sudo systemctl start asx-jobs.timer
systemctl list-timers | grep asx-jobs
```

Verification:
- Timer shows next run time.

---

## Run a manual job
```bash
sudo systemctl start asx-jobs.service
```

Verification:
```bash
sudo journalctl -u asx-jobs.service -n 50
```

---

## Check job execution
```bash
asx-jobs daily
```

Verification:
- Command exits with code 0.

Tip: `asx-jobs backfill --period 2y` is useful for seeding history.

---

## View logs
```bash
sudo journalctl -u asx-jobs.service -f
```

Related: [Feature 010](../../features/010-daily-scheduler-midday-sydney.md)
