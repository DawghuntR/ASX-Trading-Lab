# ASX Trading Lab - Deployment Guide

This directory contains deployment files for running the ASX Jobs Runner on Ubuntu 24.04 LTS.

## Systemd (Recommended)

Systemd provides better logging, restart policies, and status inspection.

### Installation

```bash
# Install Python package
cd /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs
pip install -e .

# Create environment file
cp .env.example .env
# Edit .env with your Supabase credentials

# Install systemd units
cd /home/dawghuntr/gitRepos/ASX-Trading-Lab/deploy
sudo ./install.sh
```

### Management Commands

```bash
# Start the timer
sudo systemctl start asx-jobs.timer

# Stop the timer
sudo systemctl stop asx-jobs.timer

# Check timer status
systemctl list-timers | grep asx-jobs

# Run manually
sudo systemctl start asx-jobs.service

# View logs
sudo journalctl -u asx-jobs.service -f

# View recent logs
sudo journalctl -u asx-jobs.service --since "1 hour ago"

# Check service status
sudo systemctl status asx-jobs.service
```

### Files

| File | Description |
|------|-------------|
| `systemd/asx-jobs.service` | Service unit that runs the daily job |
| `systemd/asx-jobs.timer` | Timer unit that triggers at 12:00 Sydney |
| `install.sh` | Installation script |

### Timezone Configuration

The timer runs at 12:00 **local time**. Ensure your system is set to Sydney timezone:

```bash
# Check current timezone
timedatectl

# Set to Sydney
sudo timedatectl set-timezone Australia/Sydney
```

---

## Cron (Alternative)

If you prefer cron over systemd:

### Installation

```bash
# Edit crontab
crontab -e

# Add this line (runs at 12:00 Sydney time):
0 12 * * * cd /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs && /home/dawghuntr/.local/bin/asx-jobs daily >> /var/log/asx-jobs.log 2>&1
```

### With Environment File

```bash
# Crontab entry with environment file
0 12 * * * . /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs/.env && cd /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs && /home/dawghuntr/.local/bin/asx-jobs daily >> /var/log/asx-jobs.log 2>&1
```

### Log Rotation

Create `/etc/logrotate.d/asx-jobs`:

```
/var/log/asx-jobs.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

---

## Manual Execution

Run jobs manually for testing:

```bash
# Daily run (symbols + prices + signals)
asx-jobs daily

# Backfill historical data
asx-jobs backfill --period 2y

# Symbols only
asx-jobs symbols

# Signals only (requires price data)
asx-jobs signals
```

---

## Troubleshooting

### Service won't start

1. Check environment file exists:
   ```bash
   ls -la /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs/.env
   ```

2. Check Python package is installed:
   ```bash
   which asx-jobs
   asx-jobs --help
   ```

3. Check logs:
   ```bash
   sudo journalctl -u asx-jobs.service -n 50
   ```

### Timer not firing

1. Check timer is enabled and active:
   ```bash
   systemctl status asx-jobs.timer
   ```

2. Check next scheduled run:
   ```bash
   systemctl list-timers | grep asx-jobs
   ```

3. Check system timezone:
   ```bash
   timedatectl
   ```

### Supabase connection errors

1. Verify environment variables:
   ```bash
   source /home/dawghuntr/gitRepos/ASX-Trading-Lab/jobs/.env
   echo $SUPABASE_URL
   ```

2. Test connection:
   ```bash
   curl -I "$SUPABASE_URL/rest/v1/"
   ```
