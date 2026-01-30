---
id: 010
name: Daily Scheduler (Cron/Systemd @ 12:00 Sydney)
status: Planned
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

- Daily job runs at the intended local time on Ubuntu.
- A systemd unit/timer is provided and verified workable on Ubuntu 24.04.
- A cron example is provided as a fallback.
- Logs are persisted and accessible (journald for systemd; file logs for cron if used).
- Manual re-run instructions are documented.
