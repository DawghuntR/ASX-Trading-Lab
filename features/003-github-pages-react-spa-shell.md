---
id: 003
name: GitHub Pages React SPA Shell
status: Planned
---

# 003 - GitHub Pages React SPA Shell

Create the client-side web application shell that will be deployed to GitHub Pages. This is the foundation for all UI modules (signals, symbols, backtests, portfolio/risk).

## Description

- Create a React single-page app (SPA) suitable for static hosting.
- Establish routing, layout, and baseline UI framework.
- Ensure compatibility with GitHub Pages (base path handling, SPA refresh routing).
- Integrate Supabase client initialization using public environment variables.

## Impact

- Provides an always-available, zero-server UI entry point.
- Enables rapid iteration on dashboards once data lands in Supabase.

## Success Criteria

- SPA builds successfully and runs locally.
- Client-side routes work when hosted under a subpath (GitHub Pages).
- Supabase client can connect using `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`.
- No secrets are embedded in the built frontend bundle.
