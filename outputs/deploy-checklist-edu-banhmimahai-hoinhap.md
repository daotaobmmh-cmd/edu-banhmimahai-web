# Deploy Checklist - edu.banhmimahai.vn/hoinhap

Use this checklist to track the steps for deploying the website securely.

- [ ] **1. Preparation**
  - [ ] Initialize Git repository in `edu-banhmimahai-web`
  - [ ] Create `.gitignore` to exclude scratch files, zips, and logs:
    ```
    scratch/
    _export_for_tilog/
    *.zip
    node_modules/
    .DS_Store
    ```
  - [ ] Commit all code files: `index.html`, `hoinhap/` folder

- [ ] **2. Cloudflare Pages Project Creation**
  - [ ] Create new Pages project named `edu-banhmimahai-hoinhap` via Cloudflare Dashboard
  - [ ] Set build command: *Leave blank*
  - [ ] Set output directory: `.`
  - [ ] Run the initial deploy upload

- [ ] **3. Custom Domain & DNS Setup**
  - [ ] Add `edu.banhmimahai.vn` in the Custom Domains tab of the Pages project
  - [ ] Create a CNAME record in the DNS manager:
    - Type: `CNAME`
    - Name: `edu`
    - Target: `edu-banhmimahai-hoinhap.pages.dev`
    - Proxy status: `Proxied` (Recommended)

- [ ] **4. Production Route Validation**
  - [ ] Visit `https://edu.banhmimahai.vn/` and verify redirect to `https://edu.banhmimahai.vn/hoinhap/` works
  - [ ] Open `https://edu.banhmimahai.vn/hoinhap/` and complete a test run in DevTools
  - [ ] Verify images and stylesheets render correctly without 404 errors
