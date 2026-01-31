# Troubleshooting
Fix common operator issues fast.

---

## Check journald
Use journald for systemd runs.
It captures stdout and stderr output.

```bash
sudo journalctl -u asx-jobs.service -n 100
sudo journalctl -u asx-jobs.service -f
```

---

## Fix service startup
Symptoms: `systemctl status` shows failed.
Common causes are missing env vars or a bad virtualenv.

```bash
systemctl status asx-jobs.service
ls -la /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs/.env
asx-jobs --help
```

Verification:
- Service transitions to `inactive (dead)` after a oneshot run.

---

## Fix timer not firing
Symptoms: no runs at 12:00 local time.
Check timezone and timer status.

```bash
timedatectl
systemctl status asx-jobs.timer
systemctl list-timers | grep asx-jobs
```

Verification:
- Next run time is listed.

---

## Resolve Supabase errors
Symptoms: connection errors or 401/403 responses.
Confirm URL and service role key are correct.

```bash
source /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs/.env
echo "$SUPABASE_URL"
curl -I "$SUPABASE_URL/rest/v1/"
```

Verification:
- The REST endpoint responds with `200` or `401`.

Related: [Feature 008](../../features/008-configuration-and-secrets-management.md)

---

## Investigate missing data
Symptoms: tables empty or partial after a run.
Re-run targeted jobs and watch logs.

```bash
asx-jobs symbols
asx-jobs backfill --period 2y
asx-jobs signals
```

Verification:
- Supabase tables show new rows.

Related: [Feature 015](../../features/015-data-quality-and-observability.md)

---

## Handle empty UI
Symptoms: UI loads but shows no data.
Usually the backend has not ingested data yet.

Checks:
1. Confirm jobs runner completed a daily run.
2. Confirm Supabase has data.
3. Confirm Pages build has the correct `VITE_*` variables.

Verification:
- UI shows symbol list or recent prices.

---

## Rerun tasks
Run individual tasks to isolate failures.

```bash
asx-jobs daily
asx-jobs announcements
asx-jobs paper account list
```

Related: [Jobs runner](../../jobs/README.md)

---

## Validate data in Supabase
Use the Supabase SQL editor or table view.
Focus on core tables and views.

Verification:
- `symbols` and price tables have recent timestamps.
- Views used by the UI return rows.

Related: [Feature 006](../../features/006-database-schema-v1-core.md)
