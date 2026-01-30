---
id: 001
name: GitHub Pages Web App + Homelab Signal Platform
status: Planned
---

# 001 - GitHub Pages Web App + Homelab Signal Platform

Deploy the project as a **client-side web app on GitHub Pages** while running the “heavy lifting” in a **Supabase-backed backend** (Supabase Cloud initially, with an option to migrate to self-hosted Supabase later). This establishes a scalable foundation for multiple trading decision-support subprojects: data collection, signal engines, backtesting, risk monitoring, and paper trading.

## Description

This feature is an umbrella initiative that turns the repository into a multi-component system:

Target deployment environment: **Ubuntu 24.04.3 LTS** home lab (24/7), with a static frontend deployed to GitHub Pages.

- **Frontend (GitHub Pages):** Static client-side app (React is acceptable) that visualizes data, signals, backtests, and risk metrics.
- **Backend (Supabase):** Postgres + APIs for persistence and query. Start with **Supabase Cloud** for speed; keep the design compatible with self-hosting.
- **Jobs runner (Home lab):** Ubuntu-based runner scheduled via systemd timers (preferred) or cron (acceptable) for ingestion + analytics, writing results into Supabase.

### Subprojects (planned modules)

1. **Price Movement Tracker (Signal Engine #1)**
   - Scheduled job that pulls ASX prices **daily at ~12:00 Australia/Sydney (AEST/AEDT as applicable)**.
   - Computes:
     - % change today
     - % change vs 5-day average
     - unusual volume
   - Flags momentum/abnormal movement and emits outputs (DB rows + alerts + dashboard views).

2. **Gap Up / Gap Down Detector**
   - Market-open job compares yesterday close vs today open.
   - Flags gaps above/below threshold (e.g., 3%).
   - Tracks intraday “gap fill” behavior.

3. **Volatility Spike Watcher**
   - Tracks 14-day average daily range vs today’s range.
   - Alerts when today’s range exceeds a multiplier (e.g., > 2× normal).

4. **Simple Strategy Backtester**
   - Downloads/stores historical data.
   - Simulates rule-based strategies.
   - Produces metrics: win rate, drawdown, profit, trade logs.

5. **News + Price Reaction Tracker**
   - Scrapes/ingests ASX announcements.
   - Links announcement time to subsequent price reaction (1h, 1d).
   - Aggregates patterns (e.g., cap raise → average next-day move).

6. **Personal Risk Dashboard**
   - Tracks exposure, position sizing, daily P/L, streaks.
   - Enforces risk rules with warnings when limits are breached.

7. **Paper Trading Bot (Simulation Executor)**
   - Consumes signals and places “paper” orders.
   - Tracks portfolio performance over time.
   - Provides a graduation gate (e.g., 3 months of survivable metrics) before any real-money consideration.
   - **v1 fill model:** daily close (EOD) fills.

### Enabling technology functions (cross-cutting)

- **Deployment pipeline:** Build and deploy SPA to GitHub Pages (CI/CD).
- **Backend platform:** Supabase (Cloud initially) for Postgres + APIs; auth is explicitly deferred.
- **Job scheduling:** Cron/systemd timers for periodic jobs; start with a single daily run at midday (Sydney time).
- **Data ingestion layer:** Unified adapters for price/volume/history/news sources with caching, retries, and symbol normalization.
- **Schema + persistence:** Tables for instruments, OHLCV, signals, alerts, backtests, strategies, portfolios, executions.
- **Alerting (future):** Telegram/Discord notifications with dedupe, severity, and throttling (explicitly not required for v1).
- **Observability:** Logs, job run history, and error reporting; basic health endpoints.
- **Security:** Public read-only frontend access (no auth initially). Use least-privilege access patterns (e.g., RLS + anon key + read-only views).

### Data provider (free, recommended starting point)

To meet the constraint of **free** and **recent (≤ 1 week)** data, start with:

- **Universe / symbol master:** ASX “Listed Companies” CSV (official ASX download) for the full symbol list.
- **Daily + latest quotes:** Yahoo Finance’s public endpoints (no official SLA; works without an API key) for:
  - latest quote (for “today” at midday)
  - daily historical bars (for 5-day averages, 14-day ranges, backtests)

This choice keeps costs at $0 and supports whole-of-ASX coverage by chunking requests.

#### Fallback plan

- If free quote/history endpoints become unreliable or unavailable, fall back to:
  - **ASX300 (or ASX200)** universe for v1, and/or
  - **Python web scraping via cron** to pull the minimum required daily data.

## Impact

- **Accessible UI:** Anyone with the link can load the client-side app instantly (no server to host for the UI).
- **Scalable foundation:** Home-lab services handle data collection and compute-heavy tasks without impacting the web app.
- **Decision support:** Enables systematic market scanning, learning price behavior, and validating strategies with data.
- **Incremental delivery:** Each signal engine can ship independently once the platform rails (deployment + storage + scheduling + alerts) are in place.

## Success Criteria

### Platform / deployment

- GitHub Pages hosts the latest frontend build (React SPA acceptable) from the default branch (or a dedicated pages branch) with:
  - working client-side routing (no 404 on refresh)
  - environment configuration handled safely (no secrets in the client bundle)
- Supabase Cloud is connected and holds the system-of-record data.

### Data + signals

- Scheduled jobs successfully ingest ASX price/volume data **daily at ~12:00 Australia/Sydney** and store it in the database.
- Signal engines #1–#3 produce persisted signal records with:
  - timestamp, symbol, computed metrics, and a clear “trigger reason”
  - (alerts deferred)

### Backtesting + tracking

- Backtester can run at least two defined strategies end-to-end and outputs:
  - trade log
  - summary metrics (win rate, max drawdown, total return)
- News tracker links announcements to post-event returns and can report at least one aggregated statistic.

### Risk + paper trading

- Risk dashboard computes exposure and rule violations from paper trades and/or manual inputs.
- Paper trading engine records simulated orders/fills and calculates portfolio P/L over time.

## Work Breakdown (Epic Tasks)

> This feature is an EPIC. The following tasks are the intended delivery breakdown. Status is tracked at the epic level; individual tasks are checkpoints.

### A. Product rails (required for “entire build”)

1. Frontend app scaffold (React SPA) with GitHub Pages deployment.
2. Supabase Cloud project provisioned (Postgres + API).
3. Database schema v1 created (tables + views) to support: instruments, OHLCV (daily), signals, announcements, backtests, portfolios, paper executions.
4. Public read-only access model (RLS + read-only views) for the GitHub Pages client.
5. Python jobs runner scaffold (project layout, config loading, logging, retries).
6. Scheduler configured for daily run at ~12:00 Australia/Sydney.

### B. Data ingestion (daily)

1. Universe ingestion: ASX listed companies CSV → instruments.
2. Price ingestion: daily OHLCV + “latest at midday” quote capture.
3. Backfill capability (seed last 30–90 days to enable 5-day/14-day metrics).
4. Data quality checks (missing symbols, stale data, partial updates).

### C. Analytics modules (persisted outputs)

1. Price Movement Tracker v1 (daily).
2. Volatility Spike Watcher v1 (daily).
3. Gap module decision: defer until we add market-open cadence (kept documented).

### D. Backtesting + research

1. Strategy definition format (simple rules).
2. Backtest runner v1 (at least two strategies) storing: trades + summary metrics.

### E. News + price reaction

1. ASX announcements scraper v1 (HTML scraping) with dedupe.
2. Price reaction joiner (1 day after announcement; 1 hour deferred until intraday exists).

### F. Paper trading + risk

1. Paper portfolio model v1 (EOD close fills).
2. Risk metrics v1 (exposure, position sizing summaries, streak/drawdown).

### G. UI deliverables

1. Dashboard views: latest ingest status, top signals, charts per symbol.
2. Backtest results views.
3. Portfolio/risk views.

## Runbooks / Setup & Ops (deliverables)

These are required documentation artifacts to support building and operating the system.

### Configuration (no secrets in the frontend)

- **Frontend (GitHub Pages) requires:**
  - `VITE_SUPABASE_URL` (public)
  - `VITE_SUPABASE_ANON_KEY` (public)
- **Jobs runner requires:**
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY` (secret; never shipped to the client)
  - Optional: provider-specific settings (if scraping fallback is used)

### GitHub Pages deployment

- Provide a GitHub Actions workflow that builds and deploys the SPA to GitHub Pages.
- Document how to set the frontend environment variables for the Pages build.

### Cron scheduling (Linux)

- Document a cron entry (example):
  - `0 12 * * * /usr/bin/env TZ=Australia/Sydney <run-jobs-command>`
- Document logging and failure visibility (where logs go, how to rerun).

### Supabase setup (Cloud)

- Document:
  - schema migrations / SQL to create tables + views
  - RLS policies and which views are exposed to anon
  - how to rotate keys and keep service-role secret

## Open Questions (need confirmation)

1. **Universe fallback order**: Confirmed fallback order if whole-of-ASX is impractical on free sources: **ASX300 → ASX200**.
2. **News ingestion mechanics**: Confirmed we will implement ASX announcements via HTML scraping (acknowledged as potentially brittle).

## Decisions Locked (from stakeholder input)

- **Universe:** target whole ASX; if free sources fail/unreliable, fallback to ASX300/ASX200; otherwise use Python scraping.
- **Cadence:** daily collection at ~12:00 Australia/Sydney.
- **Backend:** Supabase (confirmed).
- **Alerts:** not required for v1.
- **Public access:** public read-only for v1; auth deferred.
- **Paper trading fills (v1):** daily close (EOD).

## Feedback

- Initial scope intentionally separates **public static UI** (GitHub Pages) from **private compute** (home lab). A separate feature will capture the optional “self-hosted Supabase via Cloudflare Tunnel” path.

## Related Features (Epic Breakdown)

This EPIC is delivered via the following feature EPICs:

- 003 - GitHub Pages React SPA Shell
- 004 - GitHub Pages CI/CD Deployment
- 005 - Supabase Cloud Project Setup
- 006 - Database Schema v1 (Core)
- 007 - Public Read-Only Access (RLS + Views)
- 008 - Configuration & Secrets Management
- 009 - Python Jobs Runner Scaffold
- 010 - Daily Scheduler (Cron/Systemd @ 12:00 Sydney)
- 011 - ASX Symbol Universe Ingestion
- 012 - Free Price Data Provider Adapter (Yahoo Finance)
- 013 - Daily Price Ingestion (OHLCV + Midday Snapshot)
- 014 - Historical Backfill (Seed Window)
- 015 - Data Quality & Observability
- 016 - Signal Engine: Price Movement Tracker
- 017 - Signal Engine: Volatility Spike Watcher
- 018 - Signal Engine: Gap Up/Down Detector (Deferred)
- 019 - UI: Overview Dashboard
- 020 - UI: Symbol Drilldown
- 021 - ASX Announcements Ingestion (HTML Scraper)
- 022 - News Reaction Analytics (1D)
- 023 - Backtesting Engine v1
- 024 - Strategy Pack v1
- 025 - UI: Backtest Reporting
- 026 - Paper Trading Ledger v1 (EOD)
- 027 - Portfolio Performance Metrics
- 028 - Risk Rules & Metrics v1
- 029 - UI: Portfolio & Risk Dashboard

Self-hosting option:

- 002 - Self-Hosted Supabase via Cloudflare Tunnel
- 030 - Cloudflare Tunnel Exposure & Migration Runbook

Cross-cutting epics:

- 031 - Price Data Fallback Provider (Python Web Scraping)
- 032 - Symbol Normalization & Provider Mapping
- 033 - Local Developer Workflow & Environment
- 034 - CI Quality Gates (Frontend + Jobs Runner)
- 035 - Runbooks & Operator Documentation Pack
- 036 - Security Hardening Baseline
- 037 - Backups, Restore, and Data Retention
- 038 - Performance & Rate-Limit Management
- 039 - Legal/Non-Advisory Disclaimer & Guardrails
- 040 - Alerts & Notifications Framework (Future)
- 041 - Authentication & Private Views (Future)
