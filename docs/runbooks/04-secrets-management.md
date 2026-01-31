# Secrets
Handle keys safely across environments.

---

## Understand key roles
There are two Supabase keys with different blast radii.
Keep the service role key private at all times.

- **Anon key**: public, read-only via RLS.
- **Service role key**: private, full access.

Related: [Feature 008](../../features/008-configuration-and-secrets-management.md)

---

## Map keys to locations
Use the right key in the right place.
Never mix them.

- Frontend (GitHub Pages build): `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`.
- Jobs runner (`jobs/.env`): `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`.

Verification:
- `frontend/.env.example` contains only `VITE_*` keys.
- `jobs/.env.example` contains the service role key.

---

## Configure GitHub variables
Use repository variables for public config.
Avoid secrets for anon keys since they are public.

Steps:
1. Go to **Settings → Secrets and variables → Actions → Variables**.
2. Add `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`.

Verification:
- Pages deployment succeeds with a non-empty config.

Related: [Feature 004](../../features/004-github-pages-ci-cd-deployment.md)

---

## Keep .env files local
Never commit `.env` files to git.
Use `.env.example` as the template.

Verification:
```bash
git status --ignored
```

Tip: Add `.env` to your global gitignore if needed.

---

## Rotate keys
Rotate service role keys carefully to avoid downtime.
Plan a short maintenance window.

Steps:
1. Create a new service role key in Supabase.
2. Update `jobs/.env` on the runner host.
3. Restart the service: `sudo systemctl start asx-jobs.service`.
4. Remove the old key from Supabase.

Verification:
- `asx-jobs daily` completes successfully.
- Supabase logs show successful writes.
