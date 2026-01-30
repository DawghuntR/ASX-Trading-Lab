---
id: 004
name: GitHub Pages CI/CD Deployment
status: Planned
---

# 004 - GitHub Pages CI/CD Deployment

Automate building and deploying the frontend SPA to GitHub Pages on every change to the mainline branch.

## Description

- Add a GitHub Actions workflow to:
  - install dependencies
  - build the SPA
  - deploy to GitHub Pages
- Document required repository settings for Pages.
- Document how to provide public runtime config (Supabase URL + anon key) safely.

## Impact

- Ensures the public UI stays up to date without manual deployment.
- Makes releases reproducible.

## Success Criteria

- A workflow runs on push and produces a working Pages deployment.
- Deployment supports SPA routing (no 404 on refresh).
- Build-time environment variables are configured without exposing secrets.
