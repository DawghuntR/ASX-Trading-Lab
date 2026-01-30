---
id: 041
name: Authentication & Private Views (Future)
status: Planned
---

# 041 - Authentication & Private Views (Future)

Add authentication (Supabase Auth) and private datasets/pages when/if the platform begins to store personal or sensitive data.

## Description

- Implement login and session handling.
- Create role-based access:
  - public anonymous: read-only public views
  - authenticated user: access to private portfolio/risk or personal settings
- Update RLS accordingly.

## Impact

- Enables personalization and privacy without compromising public dashboards.

## Success Criteria

- Authenticated users can access private views.
- Anonymous users cannot access private datasets.
- RLS policies enforce separation.
