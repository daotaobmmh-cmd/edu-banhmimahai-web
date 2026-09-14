# Web UI & Frontend Standards — Edu-BanhMiMaHai OS

## 1. Brand Visual Identity (Bánh Mì Má Hải)
- **Primary Colors**:
  - Má Hải Red/Orange: `#E53935` / `#FF6F00` / `#D84315`
  - Deep Navy/Dark Slate (Header/Text): `#1E293B` / `#0F172A`
  - Accent Yellow/Gold: `#FFB300` / `#F59E0B`
  - Neutral Background: `#F8FAFC` / `#FFFFFF`
- **Typography**: Clean sans-serif fonts (`Inter`, `Roboto`, `system-ui`).
- **Responsive Layout**: Mobile-first design for employee smartphones and tablet/desktop views.

## 2. Code Quality & DOM Standards
- **HTML Validity**: Valid HTML5 semantic tags (`<header>`, `<main>`, `<section>`, `<footer>`, `<button>`, `<form>`).
- **Unique Element IDs**: All interactive quiz controls, submit buttons, and modal dialogs must have unique `id` attributes.
- **No Inline Event Handlers**: Prefer clean event listeners or modular JavaScript over inline `onclick="..."` attributes.
- **Accessibility (a11y)**: Interactive elements must have proper `aria-label`, contrast ratios, and focus states.

## 3. Performance & Asset Optimization
- **Image Assets**: Compress PNG/JPG assets; use WebP format when available.
- **No External CDN Dependencies without Fallback**: Critical CSS/JS must be available locally or cached properly for offline/weak network connectivity at store branches.
