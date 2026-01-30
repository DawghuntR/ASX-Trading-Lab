## AGENTS.md

This file is for coding agents and maintainers. It captures the practical build/test steps, repository conventions, and “gotchas” that don’t belong in the public README.

### Repo purpose (one paragraph)

ASX Trading Lab is a split-architecture system: a public, static React UI (GitHub Pages) reads from Supabase via anon key, while a private Python jobs runner writes data into Supabase using the service role key. Feature specs live in `features/`.

---

## Working directories

- Root: `/home/dawghuntr/gitRepos/ASX-Trading-Lab`
- Frontend: `frontend/`
- Jobs runner: `jobs/`
- Database migrations: `database/migrations/`
- Ops deployment: `deploy/`

---

## Build / run

### Frontend (React + Vite)

From `frontend/`:

```bash
npm install
cp .env.example .env
npm run dev
```

Build:

```bash
npm run build
```

Lint/format:

```bash
npm run lint
npm run format
```

Env vars (build-time; `VITE_` only):

- `VITE_SUPABASE_URL`
- `VITE_SUPABASE_ANON_KEY`
- `VITE_BASE_PATH` (optional; GitHub Pages base)

Safe fallback mode: if Supabase vars are missing/placeholder, `frontend/src/lib/supabase.ts` returns `supabase = null` and the UI should show empty states instead of crashing.

### Jobs runner (Python CLI)

From `jobs/`:

```bash
python -m venv .venv
source .venv/bin/activate

pip install -e .
cp .env.example .env
asx-jobs --help
```

Common commands:

```bash
asx-jobs daily
asx-jobs backfill --period 2y
asx-jobs symbols
asx-jobs announcements
asx-jobs signals

asx-jobs paper account list
asx-jobs paper metrics --account 1
asx-jobs paper risk --account 1
```

Env vars (jobs; includes secrets):

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY` (secret)
- Optional tuning: `ASX_JOBS_*`, `YAHOO_*`

---

## Tests / quality gates

From `jobs/` (dev extras):

```bash
pip install -e ".[dev]"
ruff check .
mypy src
pytest
```

From `frontend/`:

```bash
npm run build
```

---

## Conventions

### Feature documentation

- Source of truth lives in `features/`.
- Each file includes YAML frontmatter: `id`, `name`, `status`.
- When behavior changes, update the relevant feature file and cross-link from READMEs where helpful.

### Secrets and offline config

- Never commit `.env` files or keys.
- Frontend must never use service keys.
- For “offline” local UI work (no Supabase), leave frontend env vars unset and use the built-in fallback mode.

### Commit message style

Follow existing history style (short, imperative): e.g. `feat: ...`, `fix: ...`.

---

## Known dependency footnote (jobs)

`jobs/src/asx_jobs/jobs/ingest_announcements.py` imports `requests` and `bs4` (BeautifulSoup). If your environment is missing these, install:

```bash
pip install requests beautifulsoup4
```

(If you change dependencies, update `jobs/pyproject.toml` and this note.)
