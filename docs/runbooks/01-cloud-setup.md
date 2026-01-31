# Cloud setup
Launch the hosted stack with minimal friction.

---

## Confirm prerequisites
- GitHub account with Pages access.
- Supabase account with project creation rights.

Verification:
1. You can open `https://github.com/<you>/<repo>/settings/pages`.
2. You can create a project in Supabase Cloud.

---

## Prepare the repository
1. Fork the repo in GitHub.
2. Clone your fork locally.

```bash
git clone https://github.com/<you>/ASX-Trading-Lab.git
cd ASX-Trading-Lab
```

Verification:
```bash
git status
```

---

## Enable GitHub Pages
1. Go to **Settings → Pages**.
2. Set **Source** to **GitHub Actions**.
3. Save the settings.

Verification:
- Pages shows **GitHub Actions** as the source.

Related: [Feature 004](../../features/004-github-pages-ci-cd-deployment.md)

---

## Configure Pages build variables
Create repository variables in **Settings → Secrets and variables → Actions → Variables**:

- `VITE_SUPABASE_URL` = `https://<project>.supabase.co`
- `VITE_SUPABASE_ANON_KEY` = `<anon-key>`

Optional for Pages base path:
- `VITE_BASE_PATH` = `/ASX-Trading-Lab/`

Verification:
- Variables show up under **Actions → Variables**.

---

## Provision Supabase
1. Create a new Supabase project.
2. Copy the project URL and anon key.
3. Run database migrations.

Run migrations locally:
```bash
cd /home/dawghuntr/gitRepos/ASX-Trading-Lab
supabase link --project-ref <project-ref>
supabase db push
```

Verification:
- The Supabase SQL editor shows tables and views from `database/migrations/`.

Related: [Feature 005](../../features/005-supabase-cloud-project-setup.md)

---

## Wire the frontend
The frontend reads Supabase config from build-time variables.
No service role keys should be used here.

Verification:
1. Trigger a Pages build by pushing a commit.
2. Check the Actions tab for a successful deploy.

Related: [Feature 008](../../features/008-configuration-and-secrets-management.md)

---

## Verify the deployment
1. Open the Pages URL: `https://<you>.github.io/ASX-Trading-Lab/`.
2. Confirm the UI loads without errors.
3. Check that pages render empty states if data is missing.

Verification:
- No console errors about Supabase configuration.
- Dashboard pages load and show UI placeholders.

Tip: If you see empty data, run the jobs runner from the home lab guide.
