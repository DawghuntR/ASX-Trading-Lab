# Project Status

Updated: 2026-01-30

This status file is a high-level snapshot for stakeholders. Detailed specs and implementation notes live in [`features/`](./features).

## Overall

The core “rails” are in place: Supabase schema + RLS, Python jobs runner, and a GitHub Pages-ready React UI. The system supports ingestion, signals, announcements, backtests, and paper trading with portfolio/risk views.

## Completed (highlights)

- **010 - Daily Scheduler (Cron/Systemd @ 12:00 Sydney)**
- **011 - ASX Symbol Universe Ingestion**
- **012 - Free Price Data Provider Adapter (Yahoo Finance)**
- **013 - Daily Price Ingestion (OHLCV + Midday Snapshot)**
- **016 - Signal Engine: Price Movement Tracker**
- **017 - Signal Engine: Volatility Spike Watcher**
- **021 - ASX Announcements Ingestion (HTML Scraper)**
- **023 - Backtesting Engine v1**
- **024 - Strategy Pack v1**
- **025 - UI: Backtest Reporting**
- **026 - Paper Trading Ledger v1 (EOD)**
- **027 - Portfolio Performance Metrics**
- **028 - Risk Rules & Metrics v1**
- **029 - UI: Portfolio & Risk Dashboard**

See also: [`features/README.md`](./features/README.md)

## Planned / in-progress

These are documented but not considered delivered end-to-end yet:

- **015 - Data Quality & Observability** (pipeline health, alerts, monitoring)
- **018 - Signal Engine: Gap Up/Down Detector (Deferred)** (requires market-open cadence)
- **022 - News Reaction Analytics (1D)**
- **031/032 - Provider fallbacks + symbol normalization**
- **034–039 - CI, runbooks, security hardening, backups, performance, guardrails**
- **040/041 - Alerts and authentication (future)**

## Known issues / risks

- **Announcements ingestion dependencies**: the announcements job imports `requests` and `bs4` (BeautifulSoup). If they are not installed in your Python environment, `asx-jobs announcements` will fail. Workaround:
  - `pip install requests beautifulsoup4`

- **Public data exposure**: the UI is intentionally read-only and uses the Supabase anon key. RLS policies must remain enabled and reviewed whenever new tables/views are added.

- **Free provider reliability**: Yahoo Finance endpoints can rate-limit or change behavior. This is tracked in planned features (**031**, **038**).

## How to validate the system quickly

1. Apply DB migrations in Supabase (`database/migrations/*`).
2. Run `asx-jobs daily` and confirm new records in `daily_prices`, `signals`, and `announcements`.
3. Run a paper trading flow:
   - create account → submit order → execute → snapshot → metrics/risk
4. Run the frontend (`frontend/`) and verify pages:
   - `/` dashboard, `/signals`, `/symbol/:symbol`, `/backtests`, `/portfolio`
