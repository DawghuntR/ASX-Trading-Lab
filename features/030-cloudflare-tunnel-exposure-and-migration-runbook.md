---
id: 030
name: Cloudflare Tunnel Exposure & Migration Runbook
status: Planned
---

# 030 - Cloudflare Tunnel Exposure & Migration Runbook

Provide the operational documentation and configuration guidance to expose a self-hosted Supabase backend via Cloudflare Tunnel and migrate the frontend + job runner from Supabase Cloud.

## Description

Target runtime: **Ubuntu 24.04.3 LTS** home lab.

- Document the minimal set of endpoints that must be exposed for the GitHub Pages SPA.
- Provide recommended Cloudflare Tunnel routing rules to avoid exposing admin surfaces.
- Provide a migration checklist:
  - schema parity
  - data export/import
  - key and URL swap
  - validation (sample queries, UI smoke test, ingestion run)

## Impact

- Makes the “home-lab backend” goal achievable and repeatable.
- Reduces security risk by clearly defining what is and is not exposed.

## Success Criteria

- A user can follow the runbook to:
  - stand up local Supabase
  - publish required endpoints via tunnel
  - repoint the SPA and jobs runner
  - validate the system still works
