# Frontend & Visual Standards — Edu-BanhMiMaHai OS (Slice 3)

## Design Token Rules
- All brand colors must use Design Tokens (e.g. `var(--brand-red, #E53935)` or `index.css` tokens).
- Hardcoding raw hex values (such as `#E53935`, `#D32F2F`) directly inside HTML style attributes or random CSS files outside `index.css` is STRICTLY PROHIBITED (`ERR_HARDCODED_HEX_FOUND`).

## Breakpoint Testing Standards
- Mobile: 375px viewport width.
- Tablet: 768px viewport width.
- Desktop: 1440px viewport width.
- All layout changes (R1 risk) must pass 3-breakpoint Playwright screenshot testing without layout overflow.
