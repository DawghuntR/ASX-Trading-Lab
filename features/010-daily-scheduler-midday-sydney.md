---
id: 010
name: Daily Scheduler (Cron/Systemd @ 12:00 Sydney)
status: Completed
completed_date: 2026-01-30
---

# 010 - Daily Scheduler (Cron/Systemd @ 12:00 Sydney)

Schedule the daily ingestion + analytics run at ~12:00 Australia/Sydney.

## Description

- Target runtime: **Ubuntu 24.04.3 LTS** home lab, operating 24/7.

Provide **best-practice scheduling** for long-running home-lab services:

- Preferred: **systemd timer + service**
  - better logging (journald)
  - restart policies
  - easy status inspection
- Alternative: **cron** (acceptable) with documented TZ handling and log routing.

Ensure timezone correctness (Australia/Sydney) and document how to view logs and rerun manually.

## Impact

- Ensures the platform stays fresh without manual intervention.

## Success Criteria

- [x] Daily job runs at the intended local time on Ubuntu.
- [x] A systemd unit/timer is provided and verified workable on Ubuntu 24.04.
- [x] A cron example is provided as a fallback.
- [x] Logs are persisted and accessible (journald for systemd; file logs for cron if used).
- [x] Manual re-run instructions are documented.

## Implementation Notes

### Files Created

| File | Description |
|------|-------------|
| `deploy/systemd/asx-jobs.service` | Systemd service unit |
| `deploy/systemd/asx-jobs.timer` | Systemd timer unit (12:00 local) |
| `deploy/install.sh` | Installation script |
| `deploy/README.md` | Deployment documentation |

### Systemd Service Features

- Runs as user `dawghuntr`
- Structured JSON logging to journald
- Security hardening (NoNewPrivileges, ProtectSystem, etc.)
- Resource limits (1GB RAM, 50% CPU)
- 30-minute timeout

### Timer Configuration

- **Schedule**: 12:00 local time daily
- **Persistent**: Yes (catches up if system was off)
- **Random delay**: Up to 5 minutes (avoids exact scheduling issues)

### Installation

```bash
cd /home/dawghuntr/gitRepos/ASX-Trading-Lab/deploy
sudo ./install.sh
```

### Management Commands

```bash
# Start timer
sudo systemctl start asx-jobs.timer

# Check status
systemctl list-timers | grep asx-jobs

# Run manually
sudo systemctl start asx-jobs.service

# View logs
sudo journalctl -u asx-jobs.service -f
```

### Cron Alternative

```bash
# Add to crontab (crontab -e)
0 12 * * * cd /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs && /home/dawghuntr/.local/bin/asx-jobs daily >> /var/log/asx-jobs.log 2>&1
```

### Timezone Setup

```bash
# Ensure system is set to Sydney timezone
sudo timedatectl set-timezone Australia/Sydney
timedatectl
```
