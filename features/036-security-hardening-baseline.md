---
id: 036
name: Security Hardening Baseline
status: Planned
---

# 036 - Security Hardening Baseline

Establish baseline security practices for a public read-only web app backed by Supabase.

## Description

- Ensure the public client only has read access.
- Define policies for:
  - RLS usage
  - restricting exposed views/columns
  - service role key handling
  - preventing sensitive data from entering public tables
- Add a security checklist for self-host + tunnel.

## Impact

- Reduces risk of data tampering and credential leakage.

## Success Criteria

- RLS enabled on all relevant tables.
- Public anon key cannot write.
- Operator docs include a security checklist.
