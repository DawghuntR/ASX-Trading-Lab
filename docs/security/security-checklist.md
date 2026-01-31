# Hardening checklist
Actionable steps to lock down data and access.

---

## Review before deploy
Run these checks on each environment before releasing. Treat failures as blockers.

- [ ] RLS policies are applied via `database/migrations/008_rls_policies.sql`
- [ ] Frontend uses only public Supabase env vars from `frontend/.env.example`
- [ ] Jobs runner uses service role env vars from `jobs/.env.example`

---

## Secure Supabase
Confirm RLS and least-privilege access for all tables. These checks are required for public read access.

- [ ] RLS enabled on all tables:
  - instruments
  - daily_prices
  - midday_snapshots
  - signals
  - announcements
  - strategies
  - backtest_runs
  - backtest_metrics
  - backtest_trades
  - paper_accounts
  - paper_orders
  - paper_positions
  - portfolio_snapshots
- [ ] Anon key has SELECT-only policies (`TO anon FOR SELECT`) in `database/migrations/008_rls_policies.sql`
- [ ] Service role key is never referenced in frontend code or `.env` files

Verification commands:

```sql
select schemaname, tablename, rowsecurity
from pg_tables
where schemaname = 'public'
order by tablename;
```

```sql
select tablename, policyname, roles, cmd
from pg_policies
where schemaname = 'public'
order by tablename, policyname;
```

---

## Protect environments
Keep secrets out of git and off developer machines when possible. Store production secrets in a managed system.

- [ ] `.env` files are ignored by git
- [ ] Secrets are stored outside the repository (password manager or secret manager)
- [ ] GitHub Actions secrets are configured for CI/CD

Verification commands:

```bash
git check-ignore -v .env
```

```bash
gh secret list
```

---

## Harden network
Apply if you self-host the jobs runner or database. Keep inbound access narrow and monitored.

- [ ] Firewall rules allow only required ports and IPs
- [ ] Cloudflare Tunnel is configured with least-privilege routing

Verification commands:

```bash
ufw status
```

---

## Monitor and alert
Watch for access anomalies and failed policy checks. Alert on unexpected spikes or auth errors.

- [ ] Supabase logs are reviewed regularly
- [ ] Alerts exist for auth failures and unusual query volume
- [ ] Backups and restore drills are scheduled
