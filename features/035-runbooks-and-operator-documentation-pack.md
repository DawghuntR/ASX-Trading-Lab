---
id: 035
name: Runbooks & Operator Documentation Pack
status: Completed
---

# 035 - Runbooks & Operator Documentation Pack

Create operator-grade documentation for deploying, configuring, and running the entire system (cloud-first, with self-host option).

## Description

Primary deployment platform: **Ubuntu 24.04.3 LTS** home lab (24/7).

Produce runbooks covering:

- GitHub Pages deployment configuration
- Supabase Cloud provisioning + schema application
- Secrets handling (service role key, GitHub secrets)
- Home-lab jobs runner setup (systemd/cron, logging, updates)
- Troubleshooting (common failures, reruns, partial ingests)
- Self-hosted Supabase + Cloudflare Tunnel (link to Feature 002/030)

## Impact

- Makes the build reproducible and operable without tribal knowledge.

## Success Criteria

- A new operator can stand up the cloud-first system end-to-end using only the runbooks.
- A new operator can switch to self-host mode following the documented steps.
- Runbooks include Ubuntu-specific instructions for:
  - installing prerequisites
  - setting up systemd services/timers
  - viewing logs (journald)
