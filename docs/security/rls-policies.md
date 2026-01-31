# RLS guide
Protects tables with least-privilege access rules.

---

## Understand RLS
Row Level Security (RLS) enforces per-role access at the database layer. It prevents the anon key from writing or bypassing access rules.

---

## Reference current setup
RLS policies are defined in `database/migrations/008_rls_policies.sql`. This migration enables RLS on every public table and grants anon read-only access.

---

## Review protected tables
RLS is enabled on these 13 tables:

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

---

## Understand policy structure
Policies grant `SELECT` access to the `anon` role with `USING (true)`. The service role bypasses RLS by default, so it is safe only in backend jobs.

---

## Verify RLS is enabled
Use the SQL below from the Supabase SQL editor or psql. Confirm `rowsecurity` is true for all public tables.

```sql
select schemaname, tablename, rowsecurity
from pg_tables
where schemaname = 'public'
order by tablename;
```

---

## Audit access
Confirm policies and roles match the intended read-only model. Check `cmd` is `SELECT` and roles include `anon` only.

```sql
select tablename, policyname, roles, cmd
from pg_policies
where schemaname = 'public'
order by tablename, policyname;
```

---

## Related docs
See the checklist for end-to-end verification and the key guide for safe handling of Supabase keys.

- [Hardening checklist](./security-checklist.md)
- [Key management](./key-management.md)
