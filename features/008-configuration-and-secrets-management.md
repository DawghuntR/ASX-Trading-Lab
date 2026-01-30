---
id: 008
name: Configuration & Secrets Management
status: Completed
---

# 008 - Configuration & Secrets Management

Standardize how configuration is provided to the frontend and the jobs runner, with clear separation between public config and secrets.

## Description

- Define required environment variables for:
  - frontend build (public)
  - jobs runner (secrets)
- Document where each value lives:
  - GitHub repo settings / Actions secrets
  - local `.env` for the job runner (not committed)
- Define a “no secrets in frontend” rule.

## Impact

- Prevents accidental credential leaks.
- Makes setup reproducible across environments.

## Success Criteria

- Documented env var list exists and is referenced by runbooks.
- Frontend uses only Supabase public URL + anon key.
- Jobs runner uses Supabase service role key and keeps it private.

## Implementation Notes

- Frontend example config: `frontend/.env.example`
- Jobs runner example config: `jobs/.env.example`
- Frontend Supabase initialization includes placeholder detection and fallback: `frontend/src/lib/supabase.ts`
- Jobs runner config loading/validation: `jobs/src/asx_jobs/config.py`
