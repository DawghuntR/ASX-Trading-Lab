---
id: 005
name: Supabase Cloud Project Setup
status: Planned
---

# 005 - Supabase Cloud Project Setup

Provision and configure a Supabase Cloud project to serve as the system-of-record database and query layer for the GitHub Pages frontend and the home-lab job runner.

## Description

- Create a Supabase Cloud project.
- Establish required project settings for:
  - database access
  - API access
  - key management (anon vs service role)
- Document connection details and where each key is used.

## Impact

- Accelerates delivery by avoiding immediate self-host complexity.
- Provides a stable Postgres backing store for ingestion and analytics.

## Success Criteria

- Supabase project exists and is reachable from:
  - the GitHub Pages frontend (anon key)
  - the jobs runner (service role key)
- Keys are stored and referenced correctly (service role key never used in the frontend).
