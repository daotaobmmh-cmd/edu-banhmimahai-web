# Deploy Plan - edu.banhmimahai.vn/hoinhap

This document outlines the hosting architecture, DNS configuration, and verification steps for deploying the Viet Street Food Internal Training Portal.

## PROJECT SUMMARY
- **site**: Viet Street Food - Cổng Đào Tạo Nội Bộ
- **route**: `https://edu.banhmimahai.vn/hoinhap/`
- **workspace**: `D:\TRILONG-tools\website-projects\edu-banhmimahai-web`
- **app type**: Pure Static Site (HTML5 / Vanilla CSS / Tailwind CDN / AlpineJS CDN)
- **deploy root**: Workspace root (`edu-banhmimahai-web`)
- **production path**: `/hoinhap/`

## CURRENT FILE STRUCTURE
- `index.html` (Root redirect meta refresh to `./hoinhap/`)
- `skill.config.json` (Local doctrine version info)
- `hoinhap/` (Product folder containing actual application)
  - `index.html` (Application UI)
  - `app.js` (AlpineJS App logic)
  - `questions.js` (Question data source)
  - `styles.css` (Custom CSS stylesheet)
  - `screenshots/` (Updated visual QA screenshots)

## STATIC HOSTING PLAN
- **recommended platform**: Cloudflare Pages
  - *Rationale*: Free, fast global CDN, custom domain SSL support, matches other TriLong project workflows.
- **build command**: *None* (Pure static site, no compile step needed)
- **output directory**: `.` (serve the workspace root folder itself)
- **fallback/404 behavior**: Standard platform 404 response. A custom `404.html` can be added at the root.
- **root redirect strategy**: The root `index.html` uses `<meta http-equiv="refresh" content="0; url=./hoinhap/">` to instantly client-redirect traffic from `https://edu.banhmimahai.vn/` to `https://edu.banhmimahai.vn/hoinhap/`.

## DOMAIN / DNS PLAN
- **target domain**: `edu.banhmimahai.vn`
- **DNS record type**: `CNAME`
- **record name**: `edu`
- **record target**: `<pages-project-name>.pages.dev`
- **what Long must do manually**:
  1. Log into the Cloudflare Dashboard.
  2. Create a new Cloudflare Pages project (select direct upload or connect a Git repository containing the workspace).
  3. Add the custom domain `edu.banhmimahai.vn` under the project settings.
  4. Log into the DNS provider dashboard (e.g. Tino Host or Cloudflare DNS) and add the CNAME record for `edu` pointing to the project's `.pages.dev` target.
- **what AG must not do**:
  - Do not run any commands modifying active DNS zones.
  - Do not create the Cloudflare Pages project.
  - Do not read or request API keys or sensitive credentials.

## ROUTE VERIFICATION PLAN
After deploy, visual verification should check the following routes:
- `https://edu.banhmimahai.vn/` $\rightarrow$ must redirect immediately to `/hoinhap/`.
- `https://edu.banhmimahai.vn/hoinhap/` $\rightarrow$ must serve the main Gate screen.
- `https://edu.banhmimahai.vn/hoinhap/index.html` $\rightarrow$ must work identically.
- **assets**: Check DevTools network tab to ensure `styles.css`, `app.js`, `questions.js` return `200 OK` from CDN/host.
- **mobile route check**: Emulate mobile screen sizes to ensure responsive design renders correctly.

## PRE-DEPLOY RISKS
- **Path/base URL risks**: All relative paths inside `hoinhap/index.html` are prefixed with `./`. Any change in folder nesting will break references.
- **localStorage behavior**: Progress is stored per-origin in localStorage. Moving from local development to production will not carry over local debug state.
- **Cache risk**: Edge caching can hold onto old versions of the site. A version query suffix (e.g., `app.js?v=1.3`) or cache-control header should be considered for future asset updates.
- **No backend/reporting limitation**: Results are strictly local to the user's browser. There is no central database log of test scores.

## DEPLOY SLICES PROPOSED
- **Slice A — Git/repo prep only**: Initialize a git repository and commit the clean workspace.
- **Slice B — Hosting preview deploy only**: Upload to Cloudflare Pages and get a temporary `.pages.dev` preview URL.
- **Slice C — Custom domain/DNS only**: Add the custom domain and verify CNAME records.
- **Slice D — Post-deploy route verification only**: Automated Playwright test run on production URL.

## RECOMMENDATION
- **exact next approved slice to run**: **Slice A (Git/repo prep only)**
- **commands that would be needed later**:
  - `git init`, `git add .`, `git commit -m "init"` (to prep workspace for repository connection)
  - `wrangler pages deploy . --project-name=edu-banhmimahai` (if choosing CLI direct upload via Wrangler)
- **files that would be changed later**:
  - `.gitignore` (to exclude `scratch/`, `_export_for_tilog/`, `.zip` files from commits)
