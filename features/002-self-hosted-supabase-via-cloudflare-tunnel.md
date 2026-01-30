---
id: 002
name: Self-Hosted Supabase via Cloudflare Tunnel
status: Planned
---

# 002 - Self-Hosted Supabase via Cloudflare Tunnel

Enable running Supabase locally in the home lab (Docker) and exposing only the required Supabase endpoints securely to the GitHub Pages client via Cloudflare Tunnel. This is a portability feature: start with Supabase Cloud (fastest) and later migrate to self-hosting without redesigning the app.

Related feature:

- 030 - Cloudflare Tunnel Exposure & Migration Runbook

## Description

This feature adds an alternate deployment mode for the backend:

Target runtime: **Ubuntu 24.04.3 LTS** home lab.

- **Supabase (self-hosted):** Supabase Docker stack providing Postgres + REST (PostgREST) + realtime (optional) + storage (optional).
- **Cloudflare Tunnel:** A tunnel from the home network to Cloudflare that publishes selected HTTP(S) endpoints without opening inbound ports.
- **Public GitHub Pages frontend:** Uses the Supabase URL/anon key for read-only queries (auth deferred).

### Scope boundaries (v1)

- Only **database APIs** needed by the frontend are exposed.
- Everything else stays private / not advertised (“obfuscated” by lack of links and tight tunnel rules).
- Alerts are not required.
- Auth is not required.

## Impact

- **Cost control:** Removes dependence on Supabase Cloud for ongoing usage.
- **Data ownership:** Keeps the dataset fully in the home lab.
- **Architecture consistency:** Frontend and job runner code remain largely unchanged because they continue to speak “Supabase”.

## Success Criteria

- Supabase local stack runs via Docker with data persisted across restarts.
- Cloudflare Tunnel publishes a stable HTTPS URL to the required Supabase endpoints.
- GitHub Pages frontend can read required views/tables through the tunneled Supabase URL.
- Database access is constrained to read-only for the public client (e.g., RLS + read-only views).
- No secrets are embedded in the frontend beyond a Supabase **anon** key suitable for public distribution.

## Work Breakdown (Epic Tasks)

1. Choose self-host footprint (minimum: Postgres + PostgREST; optional: realtime/storage/auth).
2. Provide Docker Compose for Supabase local with persisted volumes.
3. Configure Cloudflare Tunnel to expose only required endpoints.
4. Validate GitHub Pages frontend works against tunneled Supabase URL.
5. Document migration steps from Supabase Cloud → self-host:
   - schema migration
   - data export/import
   - key/environment swap
   - validation checks

## Runbooks / Setup & Ops (deliverables)

- Docker prerequisites and how to start/stop/update the stack.
- Cloudflare Tunnel setup steps (cloudflared install, tunnel create, DNS route, config file).
- Hardening guidance:
  - do not expose the Studio/admin UI publicly
  - restrict tunnel routes to only what the SPA requires
  - keep service role key off the internet

## Open Questions (need confirmation)

1. Which Supabase components do you want to run locally (DB + REST only, or include realtime/storage/auth even if unused)?
2. Are you okay with the public client using a Supabase anon key + RLS (recommended), or do you want an additional thin API layer later to hide Supabase entirely?
3. Do you want a documented migration path (Supabase Cloud → self-hosted) included as part of this feature’s deliverable?
