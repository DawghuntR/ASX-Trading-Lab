# Key management
Handle Supabase keys safely across environments.

---

## Know the keys
Supabase provides two primary keys with different risk profiles. Treat them differently by default.

- Anon key: public, safe for frontend use when RLS is enabled
- Service role key: secret, bypasses RLS and must stay server-side

Reference files:

- `frontend/.env.example` for `VITE_SUPABASE_ANON_KEY`
- `jobs/.env.example` for `SUPABASE_SERVICE_ROLE_KEY`

---

## Store keys safely
Keep secrets outside the repository and avoid long-lived local copies. Use managed secret storage wherever possible.

- Local dev: `.env` files outside git
- CI/CD: GitHub Actions secrets
- Production: secret manager or platform vault

---

## Rotate keys
Rotate keys on a schedule and after any access change. Always update CI and deployment environments together.

1. Create new keys in Supabase settings
2. Update CI secrets and deployment config
3. Redeploy jobs runner and frontend
4. Revoke old keys after verification

---

## Respond to compromise
Assume exposure if a key lands in logs or git history. Act fast to limit blast radius.

1. Revoke the key in Supabase
2. Rotate all affected environments
3. Review logs for suspicious activity
4. Document the incident and update runbooks

---

## Configure GitHub Actions
Store secrets in GitHub so workflows can deploy safely. Use minimal scope and rotate regularly.

```bash
gh secret set VITE_SUPABASE_URL
gh secret set VITE_SUPABASE_ANON_KEY
gh secret set SUPABASE_URL
gh secret set SUPABASE_SERVICE_ROLE_KEY
```

---

## Related docs
RLS defines what anon access can do, and the checklist keeps deployments consistent.

- [RLS guide](./rls-policies.md)
- [Hardening checklist](./security-checklist.md)
