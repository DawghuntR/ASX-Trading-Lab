---
id: 003
name: GitHub Pages React SPA Shell
status: Completed
completed_date: 2026-01-30
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

- [x] SPA builds successfully and runs locally.
- [x] Client-side routes work when hosted under a subpath (GitHub Pages).
- [x] Supabase client can connect using `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`.
- [x] No secrets are embedded in the built frontend bundle.

## Implementation Notes

### Tech Stack
- React 18.3 with TypeScript 5.5
- Vite 5.4 build tool
- React Router 6.26 for client-side routing
- Supabase JS 2.45 for database connectivity

### Directory Structure
```
frontend/
├── src/
│   ├── components/   # Reusable UI components (Layout, Header, Footer, Card, StatusBadge)
│   ├── pages/        # Page components (Home, Signals, Symbol, Backtests, Portfolio, NotFound)
│   ├── lib/          # Utilities (Supabase client)
│   ├── types/        # TypeScript type definitions
│   ├── App.tsx       # Root component with routing
│   └── main.tsx      # Entry point with GitHub Pages redirect handling
├── public/
│   ├── 404.html      # SPA redirect for GitHub Pages
│   └── favicon.svg
└── package.json
```

### Key Features
- Dark theme optimized for financial data display
- Responsive design (mobile, tablet, desktop)
- Graceful degradation when Supabase is not configured
- WCAG AA accessibility compliance
- GitHub Pages SPA routing via 404.html redirect pattern

### Setup
See `frontend/README.md` for complete setup and development instructions.
