---
id: 004
name: GitHub Pages CI/CD Deployment
status: Completed
completed_date: 2026-01-30
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

- [x] A workflow runs on push and produces a working Pages deployment.
- [x] Deployment supports SPA routing (no 404 on refresh).
- [x] Build-time environment variables are configured without exposing secrets.

## Implementation Notes

### Workflow File
`.github/workflows/deploy-pages.yml`

### Triggers
- Push to `main` branch (only when `frontend/**` or workflow file changes)
- Manual trigger via `workflow_dispatch`

### Build Steps
1. Checkout code
2. Setup Node.js 20 with npm cache
3. Install dependencies (`npm ci`)
4. Type check (`tsc --noEmit`)
5. Lint (`npm run lint`)
6. Build with environment variables
7. Upload artifact to GitHub Pages

### Environment Variables (Repository Variables)
Configure these in GitHub Repository Settings → Secrets and variables → Actions → Variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | Supabase anonymous key | `eyJhbGciOiJIUzI1NiIs...` |

**Note:** These are public variables (not secrets) because the anon key is designed to be exposed in client-side code. RLS policies protect the data.

### Repository Settings Required
1. Go to Settings → Pages
2. Source: **GitHub Actions**
3. Ensure the repository has Pages enabled

### SPA Routing
The `frontend/public/404.html` file handles SPA routing by redirecting all 404s back to the main app with the original path preserved in the URL.

### Deployment URL
After deployment: `https://<username>.github.io/ASX-Trading-Lab/`
