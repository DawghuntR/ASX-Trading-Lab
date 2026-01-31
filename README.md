# ASX Trading Lab

Decision-support tooling for the Australian stock market (ASX): data ingestion, signal generation, backtesting, and paper trading — with a **static, public UI** (GitHub Pages) backed by a **Supabase Postgres** datastore and a **Python jobs runner**.

This repository is organized around feature documents in [`features/`](./features) (each feature has an ID and a markdown file).

## What this project does

- **Ingest** ASX symbol universe and daily price data.
- **Generate signals** (price movement, volatility spike).
- **Ingest announcements** from the ASX website.
- **Run backtests** and persist runs, metrics, and trades.
- **Run paper trading** (end-of-day fills), track positions, snapshots, performance, and risk status.
- **Serve a read-only web UI** that visualizes signals, backtests, and portfolio/risk.

## Architecture

```mermaid
flowchart LR
  subgraph HomeLab[Home lab / server]
    JR[Python jobs runner\n(asx-jobs)]
  end

  subgraph Supabase[Supabase (Postgres + APIs)]
    DB[(Postgres)]
    API[REST/RPC\n(RLS protected)]
  end

  subgraph Pages[GitHub Pages]
    UI[React SPA\n(read-only)]
  end

  JR -->|service role key (write)| API
  API --> DB
  UI -->|anon key (read-only)| API
```

## Repository layout

- [`frontend/`](./frontend): React + TypeScript SPA (GitHub Pages)
- [`jobs/`](./jobs): Python package + CLI (`asx-jobs`) for ingestion, signals, backtests, and paper trading
- [`database/`](./database): SQL migrations, views, and RLS policies for Supabase
- [`deploy/`](./deploy): systemd units + installation script for scheduling on Ubuntu
- [`features/`](./features): feature specs and implementation notes (source of truth)

## Prerequisites

- Node.js 18.18+ (or 20+) and npm 9+ (for `frontend/`)
- Python 3.11+ (for `jobs/`)
- A Supabase project (Cloud or self-hosted) with migrations applied

## Quick start (local)

### 1) Apply database migrations

Use the Supabase SQL Editor and run migrations in order:

- [`database/migrations/000_run_all.sql`](./database/migrations/000_run_all.sql) documents the sequence
- See [`database/README.md`](./database/README.md) for details

### 2) Configure and run the jobs runner

From `jobs/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .

cp .env.example .env
# edit jobs/.env (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

asx-jobs daily
```

Paper trading examples:

```bash
asx-jobs paper account create "My Account" --balance 100000
asx-jobs paper order buy BHP 100 --account 1
asx-jobs paper execute --date 2026-01-30
asx-jobs paper snapshot --account 1
asx-jobs paper metrics --account 1
asx-jobs paper risk --account 1
```

### 3) Configure and run the frontend

From `frontend/`:

```bash
npm install
cp .env.example .env
# edit frontend/.env (VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY)

npm run dev
```

If Supabase environment variables are missing/placeholder, the UI runs in a safe fallback mode (it will show empty states and configuration warnings).

## Deployment

- Frontend is designed for GitHub Pages (SPA routing support is included).
  See [`frontend/README.md`](./frontend/README.md) and Feature **003** / **004**.

Note: `frontend/public/404.html` contains a hard-coded redirect base path (`/ASX-Trading-Lab/`). If you deploy under a different subpath, update that file accordingly.

### GitHub Pages settings (important)

This repo deploys the frontend via **GitHub Actions** (not by serving the repository root).

In GitHub: Settings → Pages → **Source: GitHub Actions**.

If you set Pages to deploy from `main` + `/(root)`, GitHub Pages will serve the repository files (often rendering `README.md`) instead of the built SPA.

### GitLab Pages note

If you deploy this repo on GitLab Pages, you must publish the built frontend output (Vite `frontend/dist/`) as the Pages artifact.
Also set `VITE_BASE_PATH` to the project subpath used by GitLab Pages (or `/` if serving from a root domain).
- Jobs runner can be scheduled via systemd timer on Ubuntu.
  See [`deploy/README.md`](./deploy/README.md) and Feature **010**.

## Security model (read-only UI)

- The **frontend uses the Supabase anon key** and must be treated as public.
- The **jobs runner uses the Supabase service role key** and must never be committed or exposed to the browser.
- RLS is enabled on tables with public **SELECT-only** policies.
  See Feature **007** and migration `008_rls_policies.sql`.

## Documentation

- Feature index: [`features/README.md`](./features/README.md)
- Project status: [`STATUS.md`](./STATUS.md)
- Agent/developer context: [`AGENTS.md`](./AGENTS.md)

## Contributing

1. Keep feature docs current: if you change behavior, update the relevant `features/0xx-*.md`.
2. Do not commit secrets (`.env`, service keys, credentials).
3. Run checks before opening a PR:
   - `frontend/`: `npm run build` (and `npm run lint` if changing UI)
   - `jobs/`: `ruff check .`, `mypy src`, and `pytest` (where applicable)

## Related features (high-signal entry points)

- **019** - UI Overview Dashboard
- **020** - UI Symbol Drilldown
- **025** - UI Backtest Reporting
- **026** - Paper Trading Ledger v1 (EOD)
- **027** - Portfolio Performance Metrics
- **028** - Risk Rules & Metrics v1
- **029** - UI Portfolio & Risk Dashboard
