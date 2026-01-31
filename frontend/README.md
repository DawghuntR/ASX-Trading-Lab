# Frontend
Client-side shell for signals and analytics.

---
## Get started
Install dependencies, set environment values, then run the dev server.
Use the commands below from the `frontend/` directory.

```bash
npm install
cp .env.example .env
npm run dev
```

---
## Install prerequisites
Use Node.js 18.18+ or 20+ and npm 9+.
Confirm versions before you start.

```bash
node --version
npm --version
```

---
## Use scripts
Run common tasks with these npm scripts.

| Script | Purpose |
| --- | --- |
| `npm run dev` | Start the Vite dev server |
| `npm run build` | Type-check and build for production |
| `npm run preview` | Serve the production build locally |
| `npm run lint` | Run ESLint across the project |
| `npm run format` | Format source and config files |

---
## Review structure
Key folders and files are organized by purpose.

```
frontend/
├── public/
│   ├── 404.html
│   └── favicon.svg
├── src/
│   ├── components/
│   ├── lib/
│   ├── pages/
│   ├── types/
│   ├── App.tsx
│   └── main.tsx
├── .env.example
├── package.json
└── vite.config.ts
```

---
## Set variables
These values are read at build time by Vite.
Only `VITE_` prefixed variables are exposed in the browser.

| Variable | Required | Purpose |
| --- | --- | --- |
| `VITE_SUPABASE_URL` | Yes | Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Yes | Supabase public anon key |
| `VITE_BASE_PATH` | No | Base path for GitHub Pages |

Copy the example file and update the values.

```bash
cp .env.example .env
```

---
## Deploy to GitHub Pages
The app is configured for static hosting with client-side routing.
Set the base path so routes resolve under the repository subpath.

- `vite.config.ts` uses `VITE_BASE_PATH` and defaults to `/ASX-Trading-Lab/`
- `BrowserRouter` uses `import.meta.env.BASE_URL` as the basename
- `public/404.html` stores the original route and redirects to the base path
- `src/main.tsx` restores the route on reload using session storage

Tip: use `VITE_BASE_PATH=/` when building for a root domain.

### Important: keep 404 redirect base path in sync

`public/404.html` currently redirects to a hard-coded base path:

```js
const basePath = "/ASX-Trading-Lab/";
```

If you deploy under a different subpath (or a root domain), update this value to match.
For GitHub Pages the expected path is usually `/<repo-name>/`.

---
## Integrate Supabase
The client is initialized in `src/lib/supabase.ts` using public credentials.
When values are missing or placeholders, the app runs in a safe fallback mode.

```ts
import { supabase } from "@/lib/supabase"

if (supabase) {
    const { data, error } = await supabase
        .from("signals")
        .select("*")
}
```

Note: never place service keys in the frontend.

---
## Explore pages
Routes map to the React Router configuration in `src/App.tsx`.

- Dashboard (`/`): System status and top signals
- Signals (`/signals`): Daily market signals
- Symbol details (`/symbol/:symbol`): Individual stock analysis
- Backtests (`/backtests`): Strategy testing results
- Portfolio (`/portfolio`): Paper trading portfolio
- Not found (`*`): Client-side 404 page

---
## Highlight features
Key behaviors are implemented in the shell.

- React Router layout with shared header and footer
- GitHub Pages SPA refresh support
- Supabase configuration awareness with status messaging
- Modular page components with CSS modules

---
## Follow related docs
Use these references for broader context and deployment steps.

- [Feature 003: React SPA shell](../features/003-github-pages-react-spa-shell.md)
- [Feature 004: GitHub Pages deployment](../features/004-github-pages-ci-cd-deployment.md)
- [Feature 033: Local workflow](../features/033-local-developer-workflow-and-environment.md)
